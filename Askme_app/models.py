import datetime
import random

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from configuration import DELETED_USER

tags_list = ["memes", "dogs", "cats", "love", "education", "new_year", "computers", "UIKit", "Swift"]
members_list = ["kitty", "cool guy", "Roman111", "BMSTU rektor", "Evgeniy2001", "lol"]
avatars = ['img/avatar-1.jpg', 'img/avatar-2.jpg', 'img/avatar-3.jpg', 'img/no-avatar.jpg']

Popular_tags = [
    {
        'id': tag_id,
        'title': random.choice(tags_list),
    } for tag_id in range(4)
]

Best_members = [
    {
        'account_id': member_id,
        'nickname': random.choice(members_list),
    } for member_id in range(4)
]

def user_directory_path(instance, filename):
    return 'user{0}/{1}'.format(instance.user.id, filename)


class VoteManager(models.Manager):
    def is_voted(self, user, object_id):
        try:
            vote = self.filter(user=user).get(object_id=object_id)
            if vote.is_active:
                return True
        except Vote.DoesNotExist:
            pass
        return False

    def create_vote(self, user, obj, object_id, action='up-vote'):
        try:
            vote = self.filter(user=user).get(object_id=object_id)
            if vote.is_active:
                if vote.is_positive and action == 'down-vote':
                    vote.is_active = False
                    obj.total_votes -= 1
                elif not vote.is_positive and action == 'up-vote':
                    vote.is_active = False
                    obj.total_votes += 1
            else:
                if action == 'up-vote':
                    vote.is_active = True
                    vote.is_positive = True
                    obj.total_votes += 1
                elif action == 'down-vote':
                    vote.is_active = True
                    vote.is_positive = False
                    obj.total_votes -= 1
            vote.save(update_fields=['is_positive', 'is_active'])
        except Vote.DoesNotExist:
            vote = self.create(user=user, obj=obj, object_id=obj.id)
            if action == 'up-vote':
                vote.is_positive = True
                obj.total_votes += 1
            else:
                vote.is_positive = False
                obj.total_votes -= 1
            vote.save()

        obj.save(update_fields=['total_votes'])
        return vote


class ProfileManager(models.Manager):
    @staticmethod
    def update_profile_and_user(user, cleaned_data):
        user_fields, profile_fields = ['username', 'email', 'last_login', '_password'], ['bio', 'avatar']
        fields_to_update = {'user': [], 'profile': []}

        profile = Profile.objects.get(user=user.id)
        user = User.objects.get(pk=user.id)

        for key in user_fields:
            value = cleaned_data.get(key, False)
            if value:
                fields_to_update['user'].append(key)
                setattr(user, key, value)

        for key in profile_fields:
            value = cleaned_data.get(key, False)
            if value:
                fields_to_update['profile'].append(key)
                setattr(profile, key, value)

        user.save(update_fields=fields_to_update['user'])
        profile.save(update_fields=fields_to_update['profile'])

        fields_to_update = list(fields_to_update['user'] + fields_to_update['profile'])
        if fields_to_update:
            notification = Notification.objects.create(user=user, type='NEW', title='Profile updated',
                                                       text='You have updated {}.'.format(
                                                           (', '.join(fields_to_update)).replace('_', ' ')))
            notification.save()
        return user, profile


class QuestionManager(models.Manager):
    def create_question(self, **kwargs):
        user_id = kwargs['user']
        title = kwargs['title']
        text = kwargs['text']
        tags = TagManager.format_tags(kwargs['tags'])
        question = self.create(user=user_id, title=title, text=text)
        question.save()
        for tag in tags:
            current_tag = Tag.objects.create_or_update_tag(tag)
            question.tags.add(current_tag)
        return question


class AnswerManager(models.Manager):
    def create_answer(self, user, question, text, total_votes=0, is_correct=False):
        answer = self.create(user=user, question=question, text=text, total_votes=total_votes, is_correct=is_correct)
        question = Question.objects.get(pk=question.id)
        question.total_answers += 1
        question.save(update_fields=['total_answers'])
        notification = Notification.objects.create(user=question.user, type='NEW', title='New answer',
                                                   text='New answer on question "{}"'.format(question.title))
        notification.save()

        return answer


class TagManager(models.Manager):
    @staticmethod
    def format_tags(tags):
        tags = tags[:3]
        while len(tags) < 3:
            tags.append(False)
        return tags

    # TODO: transaction.atomic, select_for_update
    def create_or_update_tag(self, tag):
        try:
            tag = self.get(text=tag)
            tag.total += 1
            tag.save(update_fields=['total'])
        except Tag.DoesNotExist:
            tag = self.create(text=tag, total=1)
            tag.save()
        return tag


class Profile(User):
    objects = ProfileManager()
    login = models.TextField(max_length=100, blank=False, null=True)
    avatar = models.ImageField(upload_to=user_directory_path, default='img/no-avatar.jpg')

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tag(models.Model):
    objects = TagManager()
    text = models.CharField(max_length=15, unique=True)
    total = models.IntegerField(default=1)

    def __str__(self):
        return self.text


class Question(models.Model):
    objects = QuestionManager()

    user = models.ForeignKey(Profile, models.SET(DELETED_USER))
    title = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.datetime.now)
    text = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag)
    total_answers = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Answer(models.Model):
    objects = AnswerManager()

    user = models.ForeignKey(Profile, models.SET(DELETED_USER))
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created = models.DateTimeField(default=datetime.datetime.now)
    total_votes = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question.title


class Vote(models.Model):
    objects = VoteManager()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_positive = models.BooleanField(default=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    obj = GenericForeignKey('content_type', 'object_id')


class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    TYPE_OF_NOTIFICATIONS_CHOICES = (
        ('ERR', 'Error'),
        ('NEW', "New event"),
        ('ADM', "Tech message")
    )
    type = models.CharField(max_length=3, choices=TYPE_OF_NOTIFICATIONS_CHOICES)
    title = models.CharField(max_length=60)
    text = models.CharField(max_length=150)
    created = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title

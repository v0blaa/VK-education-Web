from Askme_app.models import Question, Notification, Answer, Tag, Profile, Vote
from django.db.models import Max, Count

def questions_for_tag(tag_name):
    return Question.objects.filter(tags__text=tag_name).order_by('-created')

def new_questions():
    sort_key = '-created'
    return Question.objects.order_by(sort_key)

def hot_questions():
    questions = Question.objects.order_by('-total_answers', '-total_votes').all()
    return questions

def answers_for_question(question_id):
    return Answer.objects.filter(question=question_id)


def tags_for_question(question):
    return question.tags.all()

def get_question_with_id(question_id):
    return Question.objects.get(id=question_id)

def popular_tags():
    tags = Tag.objects.order_by('-total').all()[:6]
    return tags
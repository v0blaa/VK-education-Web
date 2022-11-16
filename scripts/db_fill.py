from django.db import models
import random
from Askme_app.models import Question, Answer, Notification, Tag, Profile, Vote
import datetime
#
tags_list = ["memes", "dogs", "cats", "love", "education", "new_year", "computers", "UIKit", "Swift"]
members_list = ["kitty", "cool guy", "Roman111", "BMSTU rektor", "Evgeniy2001", "lol"]
avatars_path = ['static/img/avatar-1.jpg', 'static/img/avatar-2.jpg', 'static/img/avatar-3.jpg', 'static/img/no-avatar.jpg', ]

profiles_to_create =[Profile(password='123', username=f'username{id}', email=f'email{id}@mail.ru', login=f'login{id}', avatar=random.choice(avatars_path)) for id in range(2)]
#
# tags_to_create =
#
# questions_to_create =
#
# answers_to_create =
#
# votes_to_create =


def users_fill():
    User.objects.bulk_create(users_to_create)
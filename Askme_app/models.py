from django.db import models

import random

tags_list = ["memes", "dogs", "cats", "love", "education", "new_year", "computers", "UIKit", "Swift"]
members_list = ["kitty", "cool guy", "Roman111", "BMSTU rektor", "Evgeniy2001", "lol"]

Questions = [
    {
        'id': question_id,
        'autor_id': random.randint(0,2),
        'title': f'Question #{question_id}',
        'text': f'Text of the question #{question_id}',
        'answers_count': question_id * question_id,
        'rating': question_id * 100,
        'tags': tags_list[:question_id % 10],
    } for question_id in range(10)
]

Answers = [
    {
        'id': answer_id,
        'question_id': random.randint(0, len(Questions)-1),
        'text': f'Text of the answer #{answer_id}',
        'rating': random.randint(0, 100),
        'is_correct': random.choice(['checked', ''])
    } for answer_id in range(100)
]

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

Accounts = [
    {
        'account_id': 0,
        'login': "Nastya111",
        'email': "nastya111@yandex.ru",
        'nickname': "Nastya",
        'avatar_path': "img/avatar-1.jpg"
    },
    {
        'account_id': 1,
        'login': "Evgeniy2002",
        'email': "Evgeniy2002@yandex.ru",
        'nickname': "Evg",
        'avatar_path': "img/avatar-2.jpg"
    }
]
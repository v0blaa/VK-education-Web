from random import randint
import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils.datetime_safe import datetime
from faker import Faker

from Askme_app.management.commands.logger import make_logger
from Askme_app.management.commands.random_getter import get_random
from Askme_app.models import Question, Vote, Answer, Profile


class Command(BaseCommand):
    DEBUG_MODE = False

    def add_arguments(self, parser):
        parser.add_argument('answers', type=int)

        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug mode',
        )

    def handle(self, *args, **options):
        logger = make_logger(options['debug'])
        faker = Faker()
        logger.info('Generating {} answers...'.format(options['answers']))
        start_time = datetime.now().timestamp()
        total_answers = options['answers']
        i = 0
        while i < total_answers:
            user = get_random(Profile)
            question = get_random(Question)
            logger.info('Generate {} / {} answer.'.format(i + 1, options['answers']))

            answer = Answer.objects.create_answer(user=user, question=question,
                                                  text=faker.text(max_nb_chars=450, ext_word_list=None),
                                                  is_correct=bool(random.getrandbits(1)))
            answer.save()
            i += 1
            user.activity +=1
            user.save(update_fields=['activity'])

        logger.info('Operation executed in {} seconds'.format(datetime.now().timestamp() - start_time))

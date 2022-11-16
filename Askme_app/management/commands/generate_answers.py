from random import randint

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils.datetime_safe import datetime
from faker import Faker

from Askme_app.management.commands.logger import make_logger
from Askme_app.management.commands.random_getter import get_random
from Askme_app.models import Question, Vote, Answer, Profile

fake = Faker()

fake.name()


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
        total_questions = options['answers']
        i = 0
        while i < total_questions:
            user = get_random(Profile)
            question = get_random(Question)
            logger.info('Generate {} / {} answer.'.format(i + 1, options['answers']))
            question.total_answers += 1
            question.save(update_fields=['total_answers'])
            # total_votes = randint(0, MAX_VOTES_PER_ONE_ANSWER)

            answer = Answer.objects.create_answer(user=user, question=question,
                                                  text=faker.text(max_nb_chars=450, ext_word_list=None))
            answer.save()
            i += 1

        logger.info('Operation executed in {} seconds'.format(datetime.now().timestamp() - start_time))

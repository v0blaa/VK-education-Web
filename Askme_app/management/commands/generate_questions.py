from random import randint

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils.datetime_safe import datetime
from faker import Faker

from Askme_app.management.commands.logger import make_logger
from Askme_app.management.commands.random_getter import get_random
from Askme_app.models import Question, Tag, Vote, Profile


class Command(BaseCommand):
    DEBUG_MODE = False

    def add_arguments(self, parser):
        parser.add_argument('questions', type=int)
        parser.add_argument('tags', type=int)

        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug mode',
        )

    def handle(self, *args, **options):
        logger = make_logger(options['debug'])
        faker = Faker()
        logger.info('Generating {} question...'.format(options['questions']))
        start_time = datetime.now().timestamp()
        total_questions = options['questions']
        total_tags = options['tags']
        i = 0
        while i < total_questions:
            user = get_random(Profile)
            tags = get_random(Tag, total_tags)

            logger.info('Generate {} / {} question.'.format(i + 1, options['questions']))

            question = Question(user=user, title=faker.text(max_nb_chars=50),
                                text=faker.text(max_nb_chars=450, ext_word_list=None))
            question.save()
            for q in range(3):
                tag = tags[randint(0, total_tags)]
                tag.total += 1
                tag.save(update_fields=['total'])
                question.tags.add(tag)
                i += 1
        logger.info('Operation executed in {} seconds'.format(datetime.now().timestamp() - start_time))

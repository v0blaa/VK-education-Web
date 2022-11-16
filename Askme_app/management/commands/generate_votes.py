import random
from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker

from Askme_app.management.commands.logger import make_logger
from Askme_app.models import Question, Vote, Profile, Answer
from Askme_app.management.commands.random_getter import get_random
from random import randint

fake = Faker()

fake.name()

class Command(BaseCommand):
    DEBUG_MODE = False

    def add_arguments(self, parser):
        parser.add_argument('vote', type=int)
        parser.add_argument('object', type=str)

        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug mode',
        )

    def handle(self, *args, **options):
        logger = make_logger(options['debug'])
        faker = Faker()
        # logger.info('Generating {} users...'.format(options['votes']))
        total_votes = options['vote']

        model_name = options['object'].lower()

        if model_name.lower() == 'question':
            model = Question
        elif model_name.lower() == 'answer':
            model = Answer
        else:
            logger.critical('Wrong type of model. Exit.')
            return

        i = 0
        while i < total_votes:
            try:
                user = get_random(Profile)
                # logger.info('Generate vote: {}.'.format(i + 1, options['votes']))
                if model_name.lower() == 'question':
                    obj = get_random(Question)
                else:
                    obj = get_random(Answer)
                vote = Vote.objects.create_vote(user=user, obj=obj, object_id=obj.id)
                vote.save()
                i += 1
            except IntegrityError:
                logger.warning('User already exists.')

from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker

from management.commands.logger import make_logger
from models import Profile

fake = Faker()

fake.name()


class Command(BaseCommand):
    DEBUG_MODE = False

    def add_arguments(self, parser):
        parser.add_argument('users', type=int)

        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug mode',
        )

    def handle(self, *args, **options):
        logger = make_logger(options['debug'])
        fake = Faker()
        logger.info('Generating {} users...'.format(options['users']))
        total_users = options['users']
        i = 0
        while i < total_users:
            try:
                username = fake.user_name()
                logger.info('Generate {} / {} user. Name: {}.'.format(i + 1, options['users'], username))
                user = Profile(username=username, login=fake.first_name(), email=fake.email(),
                               password=fake.password())
                user.save()
                i += 1
            except IntegrityError:
                logger.warning('User already exists.')

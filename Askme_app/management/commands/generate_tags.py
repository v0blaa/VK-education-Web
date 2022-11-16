from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker

from Askme_app.management.commands.logger import make_logger
from Askme_app.models import Tag



class Command(BaseCommand):
    DEBUG_MODE = False

    def add_arguments(self, parser):
        parser.add_argument('tags', type=int)

        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug mode',
        )

    def handle(self, *args, **options):
        logger = make_logger(options['debug'])
        fake = Faker()
        logger.info('Generating {} tags...'.format(options['tags']))
        total_tags = options['tags']
        i = 0
        while i < total_tags:
            try:
                tag_name = fake.word()[:15]
                logger.info('Generate {} / {} tag. Tag name: {}.'.format(i + 1, options['tags'], tag_name))
                tag = Tag.objects.create_or_update_tag(tag=tag_name)
                tag.save()
                i += 1
            except IntegrityError:
                logger.warning('Tag already exists.')

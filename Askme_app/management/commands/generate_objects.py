from random import randint

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils.datetime_safe import datetime
from faker import Faker

from Askme_app.management.commands.logger import make_logger
from Askme_app.management.commands.random_getter import get_random
from Askme_app.models import Question, Answer, Tag, Vote

fake = Faker()

fake.name()

DEFAULT_MAX_VOTES = 1000
DEFAULT_MAX_OBJECTS = 20
DEFAULT_CHOICE_SIZE = 10


class Command(BaseCommand):
    DEBUG_MODE = False

    def add_arguments(self, parser):
        # parser.add_argument('--object', type=str)
        parser.add_argument('object', type=str)
        parser.add_argument('total', type=int)
        # parser.add_argument('--total', type=int)
        parser.add_argument('--max_votes', type=int)
        parser.add_argument('--choice-size', type=int)
        parser.add_argument('--max-objects', type=int)
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug mode',
        )

    def handle(self, *args, **options):
        start_time = datetime.now().timestamp()

        logger = make_logger(options['debug'])

        fakes = Faker()

        model_name = options['object'].lower()
        total_objects = options['total']
        max_objects_per_one_generation = options.get('max-objects') or DEFAULT_MAX_OBJECTS
        max_votes = options.get('max-max_votes') or DEFAULT_MAX_VOTES
        max_choices_size = options.get('choice-size') or DEFAULT_CHOICE_SIZE

        if model_name.lower() == 'question':
            model = Question
        elif model_name.lower() == 'answer':
            model = Answer
        else:
            logger.critical('Wrong type of model. Exit.')
            return

        generated_objects = 0
        while generated_objects < total_objects:
            users = get_random(User, max_choices_size + 1)
            if model_name == 'question':
                linked_objects = get_random(Tag, max_choices_size + 1)
            else:
                linked_objects = get_random(Question, max_choices_size + 1)

            for j in range(max_objects_per_one_generation):
                logger.info('Generate {} / {} {}.'.format(generated_objects + 1, options['total'], model_name))
                obj = model(user=users[randint(0, max_choices_size)],
                            text=fakes.text(max_nb_chars=450, ext_word_list=None))

                if model_name == 'question':
                    obj.title = fakes.text(max_nb_chars=50)
                else:
                    obj.question = linked_objects[randint(0, max_choices_size)]

                obj.save()
                total_votes = randint(0, max_votes)

                if model_name == 'question':
                    for q in range(3):
                        tag = linked_objects[randint(0, max_choices_size)]
                        tag.total += 1
                        tag.save(update_fields=['total'])
                        obj.tags.add(tag)

                for i in range(total_votes):
                    vote = Vote.objects.create_vote(user=users[randint(0, max_choices_size)], obj=obj, object_id=obj.id)
                    vote.save()
                generated_objects += 1
        logger.info('Operation executed in {} seconds'.format(datetime.now().timestamp() - start_time))

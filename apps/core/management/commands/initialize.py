import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.game.models import Question, QuestionOption

User = get_user_model()
SAMPLE_QUESTIONS = [
    {
        'text': 'What color is "Chelsea" football club first kits?',
        'wrong_options': ['White', 'Red', 'Green'],
        'correct_option': 'Blue',
    }, {
        'text': 'What color is "Manchester United" football club first kits?',
        'wrong_options': ['Pink', 'Black', 'Green'],
        'correct_option': 'Red',
    }, {
        'text': 'What color is "Real Madrid" football club first kits?',
        'wrong_options': ['Black', 'Red', 'Green'],
        'correct_option': 'White',
    }, {
        'text': 'What color is "Barcelona" football club first kits?',
        'wrong_options': ['Brown', 'Yellow', 'Green'],
        'correct_option': 'blue and garnet (deep red)',
    }, {
        'text': 'What color is "Liverpool" football club first kits?',
        'wrong_options': ['Yellow', 'Blue', 'Green'],
        'correct_option': 'Red',
    }, {
        'text': 'What color is "Arsenal" football club first kits?',
        'wrong_options': ['Yellow', 'Black', 'Grey'],
        'correct_option': 'Red',
    }, {
        'text': 'What color is "Manchester City" football club first kits?',
        'wrong_options': ['Blue', 'Black', 'White'],
        'correct_option': 'Sky Blue',
    }, {
        'text': 'What color is "Everton" football club first kits?',
        'wrong_options': ['Brown', 'Black', 'White'],
        'correct_option': 'Blue',
    }, {
        'text': 'What color is "Leicester City" football club first kits?',
        'wrong_options': ['Grey', 'Black', 'White'],
        'correct_option': 'Blue',
    },
]


class Command(BaseCommand):
    help = 'Initialize project'

    def handle(self, *args, **options):
        with transaction.atomic():
            User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='asdfqwer',
                is_staff=True,
                is_superuser=True
            )

            for question in SAMPLE_QUESTIONS:
                question_instance = Question.objects.create(
                    text=question['text'],
                    score=random.randint(5, 20)
                )

                options = ([*question['wrong_options'], question['correct_option']])
                random.shuffle(options)
                for option in options:
                    QuestionOption.objects.create(
                        question=question_instance,
                        text=option,
                        is_correct=True if option == question['correct_option'] else False
                    )

        print('============= Initialized =============')

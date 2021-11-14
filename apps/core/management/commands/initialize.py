import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.game.models import Question, QuestionOption

User = get_user_model()


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

            for question_text in 'ABCDEF':
                question = Question.objects.create(
                    text=question_text,
                    score=random.randint(5, 20)
                )

                is_correct = True
                for option_text in 'XYZ':
                    QuestionOption.objects.create(
                        question=question,
                        text=option_text,
                        is_correct=is_correct
                    )
                    is_correct = False

        print('============= Initialized =============')

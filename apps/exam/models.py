from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from helpers.models import BaseModel

User = get_user_model()


class Question(BaseModel):
    text = models.CharField(max_length=255, verbose_name=_('Text'))

    @property
    def correct_answer(self):
        try:
            return Answer.objects.get(question=self, is_correct=True)
        except Answer.DoesNotExist:
            return None

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


class Answer(BaseModel):
    text = models.CharField(max_length=255, verbose_name=_('Text'))
    question = models.ForeignKey(Question, verbose_name=_('Question'), on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField(verbose_name=_('Is Correct Answer?'))

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'is_correct'],
                condition=Q(is_correct=True),
                name='unique_correct_answer_for_each_question'
            ),
        ]


class Game(BaseModel):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='games')
    questions = models.ManyToManyField(Question, verbose_name=_('Questions Asked in This Game'), related_name='games')
    score = models.IntegerField(verbose_name=_('Final Score'))

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from helpers.models import BaseModel

User = get_user_model()


class Question(BaseModel):
    text = models.CharField(max_length=255, verbose_name=_('Text'))
    score = models.IntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(20)],
        verbose_name=_('Question Score')
    )

    @property
    def correct_option(self):
        try:
            return QuestionOption.objects.get(question=self, is_correct=True)
        except QuestionOption.DoesNotExist:
            return None

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


class QuestionOption(BaseModel):
    text = models.CharField(max_length=255, verbose_name=_('Text'))
    question = models.ForeignKey(Question, verbose_name=_('Question'), on_delete=models.CASCADE, related_name='options')
    is_correct = models.BooleanField(verbose_name=_('Is Correct?'))

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Question Option')
        verbose_name_plural = _('Question Options')
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'is_correct'],
                condition=Q(is_correct=True),
                name='unique_correct_option_for_each_question'
            ),
        ]


class Game(BaseModel):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='games')
    questions = models.ManyToManyField(Question, verbose_name=_('Questions Asked in This Game'), related_name='games')
    score = models.IntegerField(verbose_name=_('Final Score'))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')

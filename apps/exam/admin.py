from django.contrib import admin

from helpers.admin import BaseAdmin
from .forms import AnswerAdminForm
from .models import Game, Question, Answer


@admin.register(Game)
class GameAdmin(BaseAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(BaseAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(BaseAdmin):
    form = AnswerAdminForm
    raw_id_fields = ('question',)
    list_display = ('text', 'is_correct', 'question')

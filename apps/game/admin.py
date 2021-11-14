from django.contrib import admin

from helpers.admin import BaseAdmin
from .forms import QuestionOptionAdminForm
from .models import Game, Question, QuestionOption


@admin.register(Game)
class GameAdmin(BaseAdmin):
    list_display = ('__str__', 'score')
    raw_id_fields = ('user',)
    filter_horizontal = ('questions',)


@admin.register(Question)
class QuestionAdmin(BaseAdmin):
    pass


@admin.register(QuestionOption)
class QuestionOptionAdmin(BaseAdmin):
    form = QuestionOptionAdminForm
    raw_id_fields = ('question',)
    list_display = ('text', 'is_correct', 'question')

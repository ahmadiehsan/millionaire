import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.db import models
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, View, CreateView, TemplateView
from .models import Question, Game, Answer


class ExamView(TemplateView, LoginRequiredMixin):
    login_url = reverse_lazy('user:sign-in')
    http_method_names = ['get', 'post']
    template_name = 'exam/base_exam.html'

    class StepType(models.TextChoices):
        QUESTION = 'Q', _('Question')
        RESULT = 'R', _('Result')

    class Steps(models.IntegerChoices):
        FIRST = 0, _('First')
        SECOND = 1, _('Second')
        THIRD = 2, _('Third')
        FOURTH = 3, _('Fourth')
        FIFTH = 4, _('Fifth')

    def get(self, request, exam_uuid, *args, **kwargs):
        user = request.user

        if not exam_uuid:
            questions = Question.objects.all().order_by('?')[:5]
            exam_uuid = uuid.uuid4()
            game_cache_data = {
                'user_id': str(user.id),
                'current_step': self.Steps.FIRST,
                'step_type': self.StepType.QUESTION,
                'questions': [{'id': str(question.id), 'answer_id': None} for question in questions],
            }
            cache.set(exam_uuid, game_cache_data, 10 * 60 * 60)

            return HttpResponseRedirect(reverse('exam:do-exam', kwargs={'exam_uuid': exam_uuid}))

        else:
            game_cache_data = self._get_and_validate_game_cache_data(exam_uuid, user)
            context = {
                'question': self._get_question_obj_from_game_cache_data(game_cache_data),
                'step_type': game_cache_data['step_type'],
                'exam_uuid': exam_uuid
            }
            if game_cache_data['current_step'] == self.StepType.RESULT:
                answer_id = game_cache_data['questions'][game_cache_data['current_step']]['answer_id']
                context.update({'user_answer': Answer.objects.get(answer_id)})

            # if self._is_final_step(game_cache_data):
            #     Game.objects.get()

            return render(request, template_name='exam/base_exam.html', context=context)

    def post(self, request, exam_uuid, *args, **kwargs):
        user = request.user
        game_cache_data = self._get_and_validate_game_cache_data(exam_uuid, user)
        if game_cache_data['step_type'] == self.StepType.QUESTION:
            try:
                answer_id = request.POST['answer_id']
            except KeyError:
                raise ValidationError('c')

            if not self._is_final_step(game_cache_data):
                game_cache_data['questions'][game_cache_data['current_step']]['answer_id'] = answer_id
                game_cache_data['step_type'] = self.StepType.RESULT
                cache.set(exam_uuid, game_cache_data)
            else:
                question_ids = []
                final_score = 0
                for question_dict in game_cache_data['questions']:
                    question_ids.append(question_dict['id'])

                questions = Question.objects.filter(id__in=question_ids)

                for question in questions:
                    if str(question.correct_answer.id) == game_cache_data[str(question.id)]['answer_id']:
                        final_score += question.score

                Game.objects.create(
                    user_id=game_cache_data['user_id'],
                    questions=questions,
                    score=final_score
                )
                return HttpResponseRedirect(reverse('do-exam', kwargs={'exam_uuid': exam_uuid}))

        elif game_cache_data['step_type'] == self.StepType.RESULT:
            game_cache_data['step_type'] = self.StepType.QUESTION
            game_cache_data['current_step'] += 1
            cache.set(exam_uuid, game_cache_data)

        return HttpResponseRedirect(reverse('do-exam', kwargs={'exam_uuid': exam_uuid}))

    @staticmethod
    def _get_and_validate_game_cache_data(exam_uuid, user):
        game_cache_data = cache.get(exam_uuid)
        if not game_cache_data:
            raise ValidationError('a')

        if str(user.id) != game_cache_data['user_id']:
            raise ValidationError('b')

        return game_cache_data

    @staticmethod
    def _get_question_obj_from_game_cache_data(game_cache_data):
        current_question_id = game_cache_data['questions'][game_cache_data['current_step']]['id']
        try:
            question = Question.objects.get(id=current_question_id)
        except Question.DoesNotExist:
            raise ValidationError('d')
        return question

    def _is_final_step(self, game_cache_data):
        is_final_step = False
        if game_cache_data['current_step'] == self.Steps.FIFTH and game_cache_data['step_type'] == self.StepType.RESULT:
            is_final_step = True
        return is_final_step

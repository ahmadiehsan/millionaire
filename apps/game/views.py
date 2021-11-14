import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView

from .models import Question, Game, QuestionOption


class GameSpaceView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:sign-in')
    http_method_names = ['get', 'post']

    class StepTypes:
        QUESTION = 'Q'
        RESULT = 'R'

    class Steps:
        FIRST = 0
        SECOND = 1
        THIRD = 2
        FOURTH = 3
        FIFTH = 4

    def get(self, request, game_identifier, *args, **kwargs):
        user = request.user

        if game_identifier == 'new':
            questions = Question.objects.all().order_by('?')[:5]
            game_identifier = uuid.uuid4()
            cache_data = {
                'user_id': str(user.id),
                'current_step': self.Steps.FIRST,
                'current_step_type': self.StepTypes.QUESTION,
                'questions': [
                    {
                        'id': str(question.id),
                        'user_selected_option_id': None,
                        'was_correct': None,
                    } for question in questions
                ],
            }
            cache.set(game_identifier, cache_data, 10 * 60 * 60)

            return HttpResponseRedirect(reverse('game:game-space', kwargs={'game_identifier': game_identifier}))

        else:
            cache_data = self._get_and_validate_cache_data(game_identifier, user)
            question = self._get_current_question_obj_from_cache_data(cache_data)

            options = []
            if cache_data['current_step_type'] == self.StepTypes.QUESTION:
                for option in question.options.all():
                    options.append({
                        'id': str(option.id),
                        'text': option.text,
                        'html_class': 'html_class'
                    })

            elif cache_data['current_step_type'] == self.StepTypes.RESULT:
                user_selected_option_id = cache_data['questions'][cache_data['current_step']]['user_selected_option_id']

                for option in question.options.all():
                    if str(option.id) == user_selected_option_id:
                        if option.is_correct:
                            html_class = 'btn-success'
                        else:
                            html_class = 'btn-danger'
                    else:
                        if option.is_correct:
                            html_class = 'btn-primary'
                        else:
                            html_class = 'btn-outline-primary'

                    options.append({
                        'id': str(option.id),
                        'text': option.text,
                        'html_class': html_class
                    })

            context = {
                'question': question,
                'options': options,
                'display_step': cache_data['current_step'] + 1,
                'current_step_type': cache_data['current_step_type'],
                'is_final_step': self._is_final_step(cache_data),
                'game_identifier': game_identifier
            }

            return render(request, template_name='game/game_space.html', context=context)

    def post(self, request, game_identifier, *args, **kwargs):
        user = request.user
        cache_data = self._get_and_validate_cache_data(game_identifier, user)

        if cache_data['current_step_type'] == self.StepTypes.QUESTION:
            try:
                user_answer = request.POST['answer']
            except KeyError:
                raise ValidationError('c')

            if QuestionOption.objects.get(id=user_answer).is_correct:
                cache_data['questions'][cache_data['current_step']]['was_correct'] = True
            else:
                cache_data['questions'][cache_data['current_step']]['was_correct'] = False

            cache_data['questions'][cache_data['current_step']]['user_selected_option_id'] = user_answer
            cache_data['current_step_type'] = self.StepTypes.RESULT
            cache.set(game_identifier, cache_data)

        elif cache_data['current_step_type'] == self.StepTypes.RESULT:
            if not self._is_final_step(cache_data):
                cache_data['current_step_type'] = self.StepTypes.QUESTION
                cache_data['current_step'] += 1
                cache.set(game_identifier, cache_data)

            else:
                question_uuids = []
                passed_question_ids = []
                for question_dict in cache_data['questions']:
                    question_uuids.append(uuid.UUID(question_dict['id']))
                    if question_dict['was_correct']:
                        passed_question_ids.append(question_dict['id'])

                final_score = Question.objects.filter(id__in=passed_question_ids).aggregate(Sum('score'))['score__sum']
                with transaction.atomic():
                    game = Game.objects.create(
                        user_id=cache_data['user_id'],
                        score=final_score
                    )
                    game.questions.add(*question_uuids)

                cache.delete(game_identifier)
                return HttpResponseRedirect(reverse('game:result', kwargs={'game_id': game.id}))

        return HttpResponseRedirect(reverse('game:game-space', kwargs={'game_identifier': game_identifier}))

    @staticmethod
    def _get_and_validate_cache_data(game_identifier, user):
        cache_data = cache.get(game_identifier)
        if not cache_data:
            raise ValidationError('a')

        if str(user.id) != cache_data['user_id']:
            raise ValidationError('b')

        return cache_data

    @staticmethod
    def _get_current_question_obj_from_cache_data(cache_data):
        current_question_id = cache_data['questions'][cache_data['current_step']]['id']
        try:
            question = Question.objects.prefetch_related('options').get(id=current_question_id)
        except Question.DoesNotExist:
            raise ValidationError('d')

        return question

    def _is_final_step(self, cache_data):
        is_final_step = False
        if (cache_data['current_step'] == self.Steps.FIFTH and
                cache_data['current_step_type'] == self.StepTypes.RESULT):
            is_final_step = True

        return is_final_step


class ResultView(LoginRequiredMixin, TemplateView):
    template_name = 'game/result.html'
    login_url = reverse_lazy('user:sign-in')
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'game': get_object_or_404(Game, id=kwargs['game_id'])})
        return context

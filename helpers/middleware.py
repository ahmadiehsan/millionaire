from django.http import HttpResponse

from apps.game.models import Question


class CheckProjectIsConfigured:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not Question.objects.count() >= 5:
            return self._problem_in_config_response()

        for question in Question.objects.all():
            if not question.correct_option:
                return self._problem_in_config_response()

        response = self.get_response(request)
        return response

    def _problem_in_config_response(self):
        return HttpResponse('please run "python manage.py initialize" and then call project urls')

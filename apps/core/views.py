from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Max
from django.views.generic import TemplateView

from apps.game.models import Game


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'top_players': Game.objects.values(
                'user__username'
            ).annotate(max_score=Max('score')).order_by('-max_score')[:10]
        })
        return context


class TermsAndConditionsView(TemplateView):
    template_name = 'core/terms_and_conditions.html'

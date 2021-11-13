from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'core/terms_and_conditions.html'

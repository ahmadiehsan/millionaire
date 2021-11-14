from django.views.generic import TemplateView


class TermsAndConditionsView(TemplateView):
    template_name = 'core/terms_and_conditions.html'

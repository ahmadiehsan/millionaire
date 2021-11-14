from django.urls import path, reverse_lazy
from django.views.generic import RedirectView, TemplateView

app_name = 'core'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('game:statistics'), permanent=False), name='home'),
    path('terms-and-conditions/', TemplateView.as_view(template_name="core/terms_and_conditions.html"),
         name='terms-and-conditions'),
]

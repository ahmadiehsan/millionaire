from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from .views import TermsAndConditionsView

app_name = 'core'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('game:statistics'), permanent=False), name='home'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
]

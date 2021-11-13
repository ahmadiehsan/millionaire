from django.urls import path

from .views import HomeView, TermsAndConditionsView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
]

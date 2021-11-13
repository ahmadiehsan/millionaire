from django.urls import path

from .views import profile_view, SignOutView, sign_in_view, sign_up_view

app_name = 'user'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('sign-in/', sign_in_view, name='sign-in'),
    path('sign-up/', sign_up_view, name='sign-up'),
]

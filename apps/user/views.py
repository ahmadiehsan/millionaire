from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.generic import View

from .forms import SingInForm, SingUpForm, ProfileForm, ChangePasswordForm

User = get_user_model()


class SignOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)

        if request.GET.get('next'):
            redirect_url = request.GET['next']
        else:
            redirect_url = settings.LOGOUT_REDIRECT_URL

        return HttpResponseRedirect(redirect_url)


def sign_up_view(request):
    form = SingUpForm()

    if request.method == 'POST':
        form = SingUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'user/sign_up.html', {'form': form})


def sign_in_view(request):
    form = SingInForm()

    if request.method == 'POST':
        form = SingInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)

            if request.GET.get('next'):
                redirect_url = request.GET['next']
            else:
                redirect_url = settings.LOGIN_REDIRECT_URL

            return HttpResponseRedirect(redirect_url)

    return render(request, 'user/sign_in.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    profile_form = ProfileForm(instance=user)
    change_password_form = ChangePasswordForm(user=user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            profile_form = ProfileForm(data=request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, _('Profile successfully updated'))

        elif form_type == 'change_password':
            change_password_form = ChangePasswordForm(user=user, data=request.POST)
            if change_password_form.is_valid():
                user.set_password(change_password_form.cleaned_data['new_password'])
                user.save()
                messages.success(request, _('Password successfully changed'))

    return render(
        request,
        'user/profile.html',
        {
            'profile_form': profile_form,
            'change_password_form': change_password_form
        }
    )

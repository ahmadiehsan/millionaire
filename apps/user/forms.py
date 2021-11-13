from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from helpers.forms import DateInput

User = get_user_model()


class SingUpForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), help_text=_('Please enter the password again'))
    email = forms.EmailField(required=True)
    birthdate = forms.DateField(required=True, widget=DateInput())
    gender = forms.ChoiceField(choices=User.Gender.choices, widget=forms.RadioSelect)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError(_('Password fields are not equal'))

        return cleaned_data

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
            'birthdate',
            'gender',
        )


class SingInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                raise ValidationError(_('User is not active!'))
        else:
            raise ValidationError(_('Username or password is incorrect'))

        return cleaned_data


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, help_text=_('Username cannot be changed'))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    birthdate = forms.DateField(required=True, widget=DateInput())
    gender = forms.ChoiceField(choices=User.Gender.choices, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birthdate',
            'gender',
        )


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), help_text=_('Please enter the new password again'))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if not self.user.check_password(current_password):
            raise ValidationError(_('Password is incorrect'))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data['new_password']
        confirm_password = cleaned_data['confirm_password']
        if new_password != confirm_password:
            raise ValidationError(_('Password fields are not equal'))

        return cleaned_data

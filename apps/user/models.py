from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        NON_BINARY = 'N', _('Non-Binary')

    email = models.EmailField(  # This field needed to be replaced to make it 'unique = True'
        _('Email Address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists"),
        },
    )
    birthdate = models.DateField(
        _('Birthdate'),
        null=True
    )
    gender = models.CharField(
        _('Gender'),
        max_length=1,
        choices=Gender.choices,
        null=True
    )

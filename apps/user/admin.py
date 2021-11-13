from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Data'), {'fields': ('birthdate', 'gender')}),
    )


admin.site.register(User, CustomUserAdmin)

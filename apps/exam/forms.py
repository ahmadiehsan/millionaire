from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext as _

from .models import Answer


class AnswerAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['is_correct'] and cleaned_data['question'].correct_answer:
            raise ValidationError(_('Each question can only have one correct answer'))

        return cleaned_data

    class Meta:
        model = Answer
        fields = '__all__'

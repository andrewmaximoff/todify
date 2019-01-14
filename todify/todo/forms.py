import datetime

from django.utils import timezone
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Task


class TaskForm(ModelForm):
    # due_date = forms.DateField(
    #     widget=forms.SelectDateWidget,
    #     label=_('Due date'),
    #     initial=datetime.date.today,
    #     help_text=_('Due date.')
    # )

    class Meta:
        model = Task
        fields = ['title', 'body']

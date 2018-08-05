from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm
)
from .models import Person


class PersonCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = Person
        fields = ('username', 'email')


class PersonChangeForm(UserChangeForm):

    class Meta:
        model = Person
        fields = ('username', 'email')

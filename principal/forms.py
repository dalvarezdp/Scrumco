#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import Personal
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')



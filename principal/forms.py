#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import Personal, Proyecto
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        exclude = ['historiasP', 'spProyecto', 'jefeProyecto']


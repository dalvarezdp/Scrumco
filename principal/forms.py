#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import Personal, Proyecto, Historia, Tarea, Sprint, ComentarioReuniones
from django.contrib.auth.models import User


class UserForm(forms.Form):
    class Meta:
        username = forms.CharField(label='Usuario', max_length=100)
        password1 = forms.CharField(label='Contrasena', max_length=100)
        password2 = forms.CharField(label='Repite contrasena', max_length=100)
        first_name = forms.CharField(label='Nombre', max_length=100)
        last_name = forms.CharField(label='Apellidos', max_length=100)
        email = forms.EmailField(label='Email')
        telefono = forms.NumberInput()


        
class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        exclude = ['historiasP', 'spProyecto', 'jefeProyecto']
        
class HistoriaForm(ModelForm):
    class Meta:
        model = Historia
        exclude = ['proyecto', 'creador', 'estado','sprint']
        
class TareaForm(ModelForm):
    class Meta:
        model = Tarea
        exclude = ['proyecto', 'creador', 'estado','realizador','historia','esfuerzo']
        
class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        exclude = ['proyecto', 'estado', 'nTareas','hEstimadas','hPendientes','fechaFin']
        
class SelectSprintForm(forms.Form):
    class Meta:
        sprint = forms.ModelChoiceField(queryset=None,required=False)
        
class ComentarioReunionesForm(ModelForm):
    class Meta:
        model = ComentarioReuniones
        exclude = ['proyecto', 'sprint', 'persona','reunion','fecha','fechahora']


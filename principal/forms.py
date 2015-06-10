#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import Personal, Proyecto, Historia, Tarea, Sprint, ComentarioReuniones
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
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


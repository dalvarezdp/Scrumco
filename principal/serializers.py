from rest_framework import serializers
from principal.models import Tarea
 
class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ('id', 'resumen', 'descripcion','esfuerzo','estado','realizador','historia','proyecto','creador')
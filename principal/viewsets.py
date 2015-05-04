from principal.models import Tarea
from principal.serializers import TareaSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

 
class TareaViewSet(viewsets.ModelViewSet):
    
    serializer_class = TareaSerializer
    queryset = Tarea.objects.all()
    
    def retrieve(self, request, pk=None):
        tarea = self.get_object()
        queryset = Tarea.objects.all()
        tarea = get_object_or_404(queryset, pk=pk)
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)  
    

    def update(self, request, pk):
        """ Updates the object identified by the pk """
        tarea = self.get_object()
        estadoNuevo=request.DATA['estado']
        tarea.estado = estadoNuevo # your custom code
        tarea.save()
        return Response({'estado': 'cambiado'})
    
    
#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Personal(models.Model):
    fecha = models.DateTimeField(db_index=True, auto_now_add=True)
    telefono = models.IntegerField(blank="true", null="true")
    foto = models.ImageField(upload_to='perfil',verbose_name='Imágen')
    empresa = models.CharField(max_length=100, blank="False", null="False", unique="True")
    usuario = models.ForeignKey(User)
    def __unicode__(self):
        return str(self.usuario)

    
class Miembro(models.Model):
    fecha = models.DateTimeField(db_index=True, auto_now_add=True)
    telefono = models.IntegerField(blank="true", null="true")
    foto = models.ImageField(upload_to='perfil',verbose_name='Imágen')
    empresa = models.CharField(max_length=100, blank="False", null="False")
    usuario = models.ForeignKey(User)
    jefe = models.ForeignKey(Personal)
    def __unicode__(self):
        return str(self.usuario)
    

class Proyecto(models.Model):
    nombreProyecto = models.CharField(max_length=100, unique=True)
    fechaInicio = models.DateField(db_index=False, auto_now_add=False)
    descripcion = models.TextField()
    foco = models.IntegerField(blank="true", null="true")
    historiasP = models.IntegerField(blank="true", null="true")
    spProyecto = models.IntegerField(blank="true", null="true")
    jefeProyecto = models.ForeignKey(Personal)
    def __unicode__(self):
        return str(self.jefeProyecto)
    
class Sprint(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    Objetivo = models.TextField()
    fechaInicio = models.DateField(db_index=False, auto_now_add=False)
    duracion = models.IntegerField(blank="true", null="true")
    fechaRevision = models.DateField(db_index=False, auto_now_add=False)
    finSemana = models.BooleanField(default=False)
    estado = models.IntegerField(blank="true", null="true")
    nTareas = models.IntegerField(blank="true", null="true")
    hEstimadas = models.IntegerField(blank="true", null="true")
    hPendientes = models.IntegerField(blank="true", null="true")
    proyecto = models.ForeignKey(Proyecto)
    def __unicode__(self):
        return str(self.proyecto)
    

class Equipo(models.Model):
    scrummaster = models.BooleanField(default=False)
    teammember = models.BooleanField(default=True)
    productowner = models.BooleanField(default=False)
    dedicacion = models.IntegerField(blank="true", null="true")
    sprint = models.ForeignKey(Sprint, blank="true", null="true")
    proyecto = models.ForeignKey(Proyecto)
    miembro = models.ForeignKey(Miembro)
    def __unicode__(self):
        return str(self.miembro)
    

class Historia(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    prioridad = models.IntegerField(blank="true", null="true")
    sp = models.IntegerField(blank="true", null="true")
    descripcion = models.TextField()
    aceptacion = models.TextField()
    estado = models.IntegerField(blank="true", null="true")
    proyecto = models.ForeignKey(Proyecto)
    creador = models.ForeignKey(User)
    def __unicode__(self):
        return str(self.proyecto)


class Tarea(models.Model):
    resumen = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    esfuerzo = models.IntegerField(blank="true", null="true")
    estado = models.IntegerField(blank="true", null="true")
    realizador = models.ForeignKey(Equipo, blank="true", null="true")
    sprint = models.ForeignKey(Sprint, blank="true", null="true")
    historia = models.ForeignKey(Historia)
    proyecto = models.ForeignKey(Proyecto)
    creador = models.ForeignKey(User)
    def __unicode__(self):
        return str(self.historia)
    


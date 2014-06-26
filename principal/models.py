#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Personal(models.Model):
    fecha = models.DateTimeField(db_index=True, auto_now_add=True)
    telefono = models.IntegerField(blank="true", null="true")
    foto = models.ImageField(upload_to='perfil',verbose_name='Imágen')
    scrummaster = models.BooleanField(default=True)
    teammember = models.BooleanField(default=False)
    productowner = models.BooleanField(default=False)
    empresa = models.CharField(max_length=100, blank="false", null="false")
    usuario = models.ForeignKey(User)
    def __unicode__(self):
        return str(self.usuario)
#encoding:utf-8
'''
Created on 23/06/2014

@author: David
'''
from django.contrib import admin
from principal.models import Personal
from principal.models import Proyecto

# Register your models here.
admin.site.register(Personal)
admin.site.register(Proyecto)
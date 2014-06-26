from principal.models import Personal
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import re, datetime
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def inicio(request):
    usuario=request.user
    if usuario.is_authenticated():
        return render_to_response('privado.html', context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))
    
def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario,password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))


def registro(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid:
            u = formulario.save(commit=False)
            u.save()
            p = Personal.objects.create(
                foto = "default",
                usuario = u,
            )
            p.save()
            usuario = request.POST['username']
            clave = request.POST['password1']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
    return render_to_response('registro.html',{'formulario':formulario}, context_instance=RequestContext(request))
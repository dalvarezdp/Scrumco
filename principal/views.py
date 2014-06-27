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
        personal=Personal.objects.get(usuario=usuario.id)
          
    if usuario.is_authenticated():
        return render_to_response('privado.html',{'personal':personal}, context_instance=RequestContext(request))
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
            empresa = request.POST['empresa']
            usuario = request.POST['username']
            clave = request.POST['password1']
            clave2 = request.POST['password2']
            if not usuario or not clave or not clave2 or not empresa:
                return HttpResponseRedirect('/rellenarcampos')
            else:
                try:              
                    existe = User.objects.get(username=usuario)
                    return HttpResponseRedirect('/usuarioexiste')
                except:
                    try:                        
                        u = formulario.save(commit=False)
                        u.is_superuser = 1
                        u.save()
                    except:
                        return HttpResponseRedirect('/passdiferentes')
                try:
                    p = Personal.objects.create(
                        foto = "default",
                        usuario = u,
                        empresa = request.POST['empresa']
                    )
                    p.save()
                except:
                    e = User.objects.get(username=usuario)
                    e.delete()
                    return HttpResponseRedirect('/empresaexiste')                  
                acceso = authenticate(username=usuario, password=clave)
                if acceso is not None:
                    if acceso.is_active:
                        login(request, acceso)
                        return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/ingresar')
    else:
        formulario = UserCreationForm()
    return render_to_response('registro.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')
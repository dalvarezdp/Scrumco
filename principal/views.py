from principal.models import Personal, Miembro, Proyecto, Equipo, historia
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import re
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from forms import ProyectoForm, UserForm, HistoriaForm
# Create your views here.

def inicio(request):
    usuario=request.user
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
          
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
            return HttpResponseRedirect('/noFormularioValido')
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))


def registro(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
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

@login_required(login_url='/ingresar')
def lista_miembros(request):
    usuario=request.user
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            miembros = Miembro.objects.filter(jefe=personal.id)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            miembros = Miembro.objects.filter(jefe=personal.jefe)
          
    if usuario.is_authenticated():
        return render_to_response('miembros.html',{'personal':personal, 'miembros':miembros}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))
    

@login_required(login_url='/ingresar')   
def nuevo_miembro(request):
    usuario=request.user
    if usuario.is_authenticated():
        personal=Personal.objects.get(usuario=usuario.id)
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            usuario = request.POST['username']
            clave = request.POST['password1']
            clave2 = request.POST['password2']
            nombre = request.POST['first_name']
            apellidos = request.POST['last_name']
            email = request.POST['email']
            if not usuario or not clave or not clave2:
                return HttpResponseRedirect('/rellenarcampos')
            else:
                try:              
                    existe = User.objects.get(username=usuario)
                    return HttpResponseRedirect('/usuarioexiste')
                except:
                    try:                        
                        u = formulario.save(commit=False)
                        u.first_name = nombre
                        u.last_name = apellidos
                        u.email = email
                        u.save()
                    except:
                        return HttpResponseRedirect('/passdiferentes')
                
                m = Miembro.objects.create(
                    foto = "default",
                    usuario = u,
                    jefe = personal,
                    empresa = personal.empresa
                )
                m.save()                  
                return HttpResponseRedirect('/miembros')
        else:
            return HttpResponseRedirect('/noFormularioValido')
    else:
        formulario = UserCreationForm()
    return render_to_response('registromiembro.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def lista_proyectos(request):
    usuario=request.user
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            proyectos=Proyecto.objects.filter(jefeProyecto=personal.id)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            proyectos=Equipo.objects.filter(miembro=personal.id)
          
    if usuario.is_authenticated():
        return render_to_response('proyectos.html',{'personal':personal, 'proyectos':proyectos}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))
    

@login_required(login_url='/ingresar')    
def nuevo_proyecto(request):
    usuario=request.user
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            miembros = Miembro.objects.filter(jefe=personal.id)
    if request.method == 'POST':
        formulario=ProyectoForm(request.POST)
        if formulario.is_valid():
            nombreProyecto = request.POST['nombreProyecto']
            fechaInicio = request.POST['fechaInicio']
            #if fechaInicio:
            #    fecha =  datetime.strptime(fechaInicio,"%d/%m/%Y").strftime("%Y-%m-%d")           
            descripcion = request.POST['descripcion']
            foco = request.POST['foco']
            equipo = request.POST.getlist('equipo')
            if not nombreProyecto or not fechaInicio or not descripcion or not equipo:
                return HttpResponseRedirect('/rellenarcampos')
            else:
                try:              
                    existe = Proyecto.objects.get(nombreProyecto=nombreProyecto)
                    return HttpResponseRedirect('/proyectoexiste')
                except:
                    #try:                        
                        p=formulario.save(commit=False)
                        p.historiasP = 0
                        p.spProyecto = 0
                        p.jefeProyecto = personal
                        p.save()
                    #except:
                        #return HttpResponseRedirect('/passdiferentes')
                
                for dato in equipo:
                    e = Equipo.objects.create(                       
                        proyecto = p,
                        miembro = Miembro.objects.get(id=dato),
                    )
                    e.save()                  
            return HttpResponseRedirect('/proyectos')
        else:
            return HttpResponseRedirect('/formularioNoValido')
    else:
        formulario = ProyectoForm()
    return render_to_response('registroproyecto.html',{'formulario':formulario, 'personal':personal, 'miembros':miembros}, context_instance=RequestContext(request))



@login_required(login_url='/ingresar')    
def detalle_proyecto(request, id_proyecto):
    usuario=request.user
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(id=id_proyecto)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(id=id_proyecto)
          
    if usuario.is_authenticated():
        return render_to_response('detalleproyecto.html', {'personal':personal, 'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))
    
    
@login_required(login_url='/ingresar')    
def lista_historias(request, id_proyecto):
    usuario=request.user
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(id=id_proyecto)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(id=id_proyecto)
          
    if usuario.is_authenticated():
        return render_to_response('historias.html', {'personal':personal, 'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))


@login_required(login_url='/ingresar')    
def nueva_historia(request, id_proyecto):
    usuario=request.user
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        formulario=HistoriaForm(request.POST)
        if formulario.is_valid():
            titulo = request.POST['titulo']
            #if fechaInicio:
            #    fecha =  datetime.strptime(fechaInicio,"%d/%m/%Y").strftime("%Y-%m-%d")           
            sp = request.POST['sp']
          
            if not titulo:
                return HttpResponseRedirect('/rellenarcampos')
            else:
                try:              
                    existe = historia.objects.get(titulo=titulo)
                    return HttpResponseRedirect('/historiaexiste')
                except:
                    #try:                        
                        p=formulario.save(commit=False)
                        p.proyecto = proyecto
                        p.creador = usuario
                        p.save()
                    #except:
                        #return HttpResponseRedirect('/passdiferentes')
                        e = Proyecto.objects.get(pk=id_proyecto)
                        e.historiasP += 1
                        e.spProyecto += int(sp)
                        e.save()
            
            return HttpResponseRedirect(reverse('lista_historias',args=[id_proyecto]))            
        else:
            return HttpResponseRedirect('/formularioNoValido')
    else:
        formulario = HistoriaForm()
    return render_to_response('registrohistoria.html',{'formulario':formulario, 'personal':personal}, context_instance=RequestContext(request))






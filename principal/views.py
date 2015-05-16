from principal.models import Personal, Miembro, Proyecto, Equipo, Historia, Tarea, Sprint, Poker
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
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from forms import ProyectoForm, UserForm, HistoriaForm, TareaForm, SprintForm, SelectSprintForm

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
                    m = Miembro.objects.create(
                        foto = "default",
                        usuario = u,
                        jefe = p,
                        empresa = request.POST['empresa']
                    )
                    m.save()
                  
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
            miembros = Miembro.objects.filter(jefe=personal.id).exclude(usuario=personal.usuario)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            miembros = Miembro.objects.filter(jefe=personal.jefe).exclude(usuario=personal.jefe.usuario)
          
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
    proyecto=Proyecto.objects.get(id=id_proyecto)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            historias=Historia.objects.filter(proyecto_id=id_proyecto)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            historias=Historia.objects.filter(proyecto_id=id_proyecto)
          
    if usuario.is_authenticated():
        return render_to_response('historias.html', {'personal':personal, 'historias':historias, 'proyecto':proyecto}, context_instance=RequestContext(request))
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
                    existe = Historia.objects.get(titulo=titulo)
                    return HttpResponseRedirect('/historiaexiste')
                except:
                    #try:                        
                        p=formulario.save(commit=False)
                        p.estado = 0
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
    return render_to_response('registrohistoria.html',{'formulario':formulario, 'personal':personal, 'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')    
def detalle_historia(request, id_historia):
    usuario=request.user
    historia=Historia.objects.get(id=id_historia)
    proyecto=Proyecto.objects.get(id=historia.proyecto.id)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            tareas=Tarea.objects.filter(historia_id=id_historia)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            tareas=Tarea.objects.filter(historia_id=id_historia)
          
    if usuario.is_authenticated():
        return render_to_response('detallehistoria.html', {'personal':personal, 'tareas':tareas, 'proyecto':proyecto, 'historia':historia}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))

@login_required(login_url='/ingresar')    
def nueva_tarea(request, id_proyecto, id_historia):
    usuario=request.user
    historia=Historia.objects.get(pk=id_historia)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(pk=id_proyecto)
    
    if request.method == 'POST':
        formulario=TareaForm(request.POST)
        if formulario.is_valid():
            resumen = request.POST['resumen']           
            descripcion = request.POST['descripcion']
          
            if not resumen:
                return HttpResponseRedirect('/rellenarcampos')
            else:                     
                p=formulario.save(commit=False)
                p.estado = 0
                p.historia = historia
                p.proyecto = proyecto
                p.creador = usuario
                p.save()                    
            
            return HttpResponseRedirect(reverse('detalle_historia',args=[id_historia]))            
        else:
            return HttpResponseRedirect('/formularioNoValido')
    else:
        formulario = TareaForm()
    return render_to_response('registrotarea.html',{'formulario':formulario, 'personal':personal, 'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')    
def lista_sprints(request, id_proyecto):
    usuario=request.user
    proyecto=Proyecto.objects.get(id=id_proyecto)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
          
    if usuario.is_authenticated():
        return render_to_response('sprints.html', {'personal':personal, 'sprints':sprints, 'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))


@login_required(login_url='/ingresar')    
def nuevo_sprint(request, id_proyecto):
    dedicaciones=[]
    usuario=request.user
    if usuario.is_authenticated():
        if usuario.is_superuser:
            proyecto=Proyecto.objects.get(id=id_proyecto)
            personal=Personal.objects.get(usuario=usuario.id)
            equipo = Equipo.objects.filter(proyecto_id=id_proyecto).order_by('id')
            historias=Historia.objects.filter(proyecto_id=id_proyecto).filter(sprint_id=None)

    if request.method == 'POST':
        formulario=SprintForm(request.POST)
        if formulario.is_valid():
            nombreSprint = request.POST['nombre']
            fechaInicio = request.POST['fechaInicio']
            objetivo = request.POST['Objetivo']
            duracion = request.POST['duracion']
            fechaRevision = request.POST['fechaRevision']
            finSemana = request.POST['finSemana']
            historiasSprint = request.POST.getlist('historiasSprint')
            
            fechaInicio = datetime.strptime(fechaInicio,'%Y-%m-%d')
            
            print historiasSprint
            print fechaInicio
            
            fechaFin = fechaInicio + timedelta(days=(7*(int(duracion))))
            
            print fechaFin
            
            for dato in equipo:
                dedicaciones.append(request.POST['foco_'+str(dato.id)])  

            #if fechaInicio:
            #    fecha =  datetime.strptime(fechaInicio,"%d/%m/%Y").strftime("%Y-%m-%d")           
            
            if not nombreSprint or not fechaInicio or not objetivo:
                return HttpResponseRedirect('/rellenarcampos')
            else:
                try:              
                    existe = Sprint.objects.get(nombre=nombreSprint)
                    return HttpResponseRedirect('/sprintexiste')
                except:
                    #try:                       
                        p=formulario.save(commit=False)
                        p.fechaFin = fechaFin
                        p.estado = 1
                        p.nTareas = 0
                        p.hEstimadas = 0
                        p.hPendientes = 0
                        p.proyecto = proyecto
                        p.save()
                    #except:
                        #return HttpResponseRedirect('/passdiferentes')
                        
                        #Agrego al equipo la dedicacion y el sprint
                        for i in range(len(equipo)):
                            equipo[i].dedicacion = dedicaciones[i]
                            equipo[i].sprint = p
                            equipo[i].save() 
                        
                        for dato in historiasSprint: 
                            historia = Historia.objects.get(id=dato)   
                            print historia        
                            historia.sprint = p
                            historia.save()
                            
                                  
            return HttpResponseRedirect(reverse('lista_sprints',args=[id_proyecto]))
        else:
            return HttpResponseRedirect('/formularioNoValido')
    else:
        formulario = SprintForm()
    return render_to_response('registrosprint.html',{'formulario':formulario, 'personal':personal, 'equipo':equipo, 'historias':historias, 'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')    
def detalle_sprint(request, id_sprint):
    usuario=request.user
    sprint = Sprint.objects.get(id=id_sprint)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(id=sprint.proyecto_id)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(id=sprint.proyecto_id)
          
    if usuario.is_authenticated():
        return render_to_response('detallesprint.html', {'personal':personal, 'proyecto':proyecto, 'sprint':sprint}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))
    
    
@login_required(login_url='/ingresar')    
def calendario(request, id_proyecto):
    usuario=request.user
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(id=id_proyecto)
            sprints=Sprint.objects.filter(proyecto=id_proyecto)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(id=id_proyecto)
            sprints=Sprint.objects.filter(proyecto=id_proyecto)
          
    if usuario.is_authenticated():
        return render_to_response('calendario.html', {'personal':personal, 'proyecto':proyecto, 'sprints':sprints}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))
    
    

@login_required(login_url='/ingresar')    
def lista_sprintbacklog(request, id_sprint):
    usuario=request.user
    sprint = Sprint.objects.get(id=id_sprint)
    historias=Historia.objects.filter(sprint=id_sprint)
    proyecto=Proyecto.objects.get(id=sprint.proyecto.id)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            tareas=Tarea.objects.filter(historia__in=historias)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            tareas=Tarea.objects.filter(historia__in=historias)
            
    formulario = TareaForm()
          
    if usuario.is_authenticated():
        return render_to_response('sprintbacklog.html', {'formulario':formulario, 'personal':personal, 'tareas':tareas, 'proyecto':proyecto, 'historias':historias, 'sprint':sprint}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))

@login_required(login_url='/ingresar')    
def nueva_tarea_modal(request, id_proyecto, id_historia):
    print id_historia
    usuario=request.user
    historia=Historia.objects.get(pk=id_historia)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            proyecto=Proyecto.objects.get(pk=id_proyecto)
    
    if request.method == 'POST':
        formulario=TareaForm(request.POST)
        if formulario.is_valid():
            resumen = request.POST['resumen']           
            descripcion = request.POST['descripcion']
          
            if not resumen:
                return HttpResponseRedirect('/rellenarcampos')
            else:                     
                p=formulario.save(commit=False)
                p.estado = 0
                p.historia = historia
                p.proyecto = proyecto
                p.creador = usuario
                p.save()                    
            
            return HttpResponseRedirect(reverse('lista_sprintbacklog',args=[historia.sprint_id]))            
        else:
            return HttpResponseRedirect('/formularioNoValido')
    else:
        formulario = TareaForm()
    return render_to_response('registrotarea.html',{'formulario':formulario, 'personal':personal, 'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')    
def ver_muro(request, id_sprint):
    usuario=request.user
    sprint = Sprint.objects.get(id=id_sprint)
    historias=Historia.objects.filter(sprint=id_sprint)
    proyecto=Proyecto.objects.get(id=sprint.proyecto.id)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Personal.objects.get(usuario=usuario.id)
            tareas=Tarea.objects.filter(historia__in=historias)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            tareas=Tarea.objects.filter(historia__in=historias)
          
    if usuario.is_authenticated():
        return render_to_response('muro.html', {'personal':personal, 'tareas':tareas, 'proyecto':proyecto, 'historias':historias, 'sprint':sprint}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))


@login_required(login_url='/ingresar')    
def sprints_poker(request, id_proyecto):
    usuario=request.user
    proyecto=Proyecto.objects.get(id=id_proyecto)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Miembro.objects.get(usuario=usuario.id)
            sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
            personaEquipo=Equipo.objects.get(miembro=personal.id)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
            personaEquipo=Equipo.objects.get(miembro=personal.id)
            
    if request.method == 'POST':
        formulario=SelectSprintForm(request.POST)
        if formulario.is_valid():
            id_sprint = request.POST['sprint']
            sprint = Sprint.objects.get(id=id_sprint)           
            historias = Historia.objects.filter(sprint = id_sprint)
            tareas=Tarea.objects.filter(historia__in=historias)
            
                       
            
            return HttpResponseRedirect(reverse('planning_poker',args=[id_proyecto,sprint.id]))
        else:
            return HttpResponseRedirect('/formularioNoValido')
    else:
        formulario = SelectSprintForm()
    
          
    if usuario.is_authenticated():
        return render_to_response('sprintpoker.html', {'personaEquipo':personaEquipo,'personal':personal, 'sprints':sprints, 'proyecto':proyecto, 'formulario':formulario}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))    


@login_required(login_url='/ingresar')    
def planning_poker(request,id_proyecto, id_sprint):
    usuario=request.user
    proyecto=Proyecto.objects.get(id=id_proyecto)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Miembro.objects.get(usuario=usuario.id)
            sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
            personaEquipo=Equipo.objects.get(miembro=personal.id)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
            personaEquipo=Equipo.objects.get(miembro=personal.id)
        
        sprint = Sprint.objects.get(id=id_sprint)                     
        historias = Historia.objects.filter(sprint = id_sprint)
        tareas=Tarea.objects.filter(historia__in=historias)
        
        historiasVotadas=Poker.objects.filter(jugador_id=personaEquipo.id)
        
        if request.method == 'POST':
            formulario=SelectSprintForm(request.POST)
            if formulario.is_valid():
                id_sprint = request.POST['sprint']
                sprint = Sprint.objects.get(id=id_sprint)           
                historias = Historia.objects.filter(sprint = id_sprint)
                tareas=Tarea.objects.filter(historia__in=historias)
                
                           
                
                return HttpResponseRedirect(reverse('planning_poker',args=[id_proyecto,sprint.id]))
            else:
                return HttpResponseRedirect('/formularioNoValido')
        else:
            formulario = SelectSprintForm()
    
          
    if usuario.is_authenticated():
        return render_to_response('poker.html', {'historiasVotadas':historiasVotadas,'personaEquipo':personaEquipo,'personal':personal, 'sprints':sprints, 'valueSprint':sprint, 'historias':historias, 'tareas':tareas, 'proyecto':proyecto, 'formulario':formulario}, context_instance=RequestContext(request))
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request))    
    
    
    
@login_required(login_url='/ingresar')    
def votar_poker(request, id_proyecto, id_sprint, id_historia, voto):
    usuario=request.user
    proyecto=Proyecto.objects.get(id=id_proyecto)
    sprint=Sprint.objects.get(id=id_sprint)
    historia=Historia.objects.get(id=id_historia)
    if usuario.is_authenticated():
        if usuario.is_superuser:
            personal=Miembro.objects.get(usuario=usuario.id)
            sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
            personaEquipo=Equipo.objects.get(miembro=personal.id)
        else:
            personal=Miembro.objects.get(usuario=usuario.id)
            sprints=Sprint.objects.filter(proyecto_id=id_proyecto)
            personaEquipo=Equipo.objects.get(miembro=personal.id)
            
            
        try:              
            existe = Poker.objects.get(jugador=personaEquipo,proyecto_id=id_proyecto,sprint_id=id_sprint,historia_id=id_historia)
            existe.delete()
            
            v = Poker.objects.create(                       
                proyecto = proyecto,
                sprint = sprint,
                historia = historia,
                votado = 1,
                spVotado = voto,
                jugador = personaEquipo,
            )
            v.save() 
        except:                     
            v = Poker.objects.create(                       
                proyecto = proyecto,
                sprint = sprint,
                historia = historia,
                votado = 1,
                spVotado = voto,
                jugador = personaEquipo,
            )
            v.save()  
    
          
    if usuario.is_authenticated():
         return HttpResponseRedirect(reverse('planning_poker',args=[id_proyecto,id_sprint])) 
    else:
        return render_to_response('inicio.html', context_instance=RequestContext(request)) 
    


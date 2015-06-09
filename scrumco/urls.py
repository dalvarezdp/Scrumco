from django.conf.urls import patterns, include, url
from django.conf import settings
from principal.viewsets import TareaViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tareas', TareaViewSet)

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scrumco.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api/tienda/SFID/(?P<SFID>\d+)$','principal.views.tienda_sfid', name='tienda_sfid'),
    

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'principal.views.inicio'),
    #url(r'^privado','principal.views.privado'),
    url(r'^ingresar', 'principal.views.ingresar'),
    url(r'^registro', 'principal.views.registro'),
    url(r'^cerrar','principal.views.cerrar'),
    url(r'^miembros', 'principal.views.lista_miembros'),
    url(r'^miembro/nuevo/$', 'principal.views.nuevo_miembro'),
    url(r'^proyectos', 'principal.views.lista_proyectos'),
    url(r'^proyecto/nuevo/$', 'principal.views.nuevo_proyecto'),
    #url(r'^rolequipo/$', 'principal.views.rol_equipo'),
    url(r'^proyecto/(?P<id_proyecto>\d+)$','principal.views.detalle_proyecto', name='detalle_proyecto'),
    url(r'^historia/(?P<id_historia>\d+)$','principal.views.detalle_historia', name='detalle_historia'),
    url(r'^historias/(?P<id_proyecto>\d+)$', 'principal.views.lista_historias', name='lista_historias'),   
    url(r'^historia/nueva/(?P<id_proyecto>\d+)$', 'principal.views.nueva_historia', name='nueva_historia'),
    url(r'^tarea/nueva/py/(?P<id_proyecto>\d+)/ht/(?P<id_historia>\d+)$', 'principal.views.nueva_tarea', name='nueva_tarea'),
    url(r'^sprint/tarea/nueva/py/(?P<id_proyecto>\d+)/ht/(?P<id_historia>\d+)$', 'principal.views.nueva_tarea_modal', name='nueva_tarea_modal'),
    url(r'^sprints/(?P<id_proyecto>\d+)$', 'principal.views.lista_sprints', name='lista_sprints'), 
    url(r'^sprint/(?P<id_sprint>\d+)$','principal.views.detalle_sprint', name='detalle_sprint'),
    url(r'^sprint/backlog/(?P<id_sprint>\d+)$','principal.views.lista_sprintbacklog', name='lista_sprintbacklog'),
    url(r'^sprint/nuevo/(?P<id_proyecto>\d+)$', 'principal.views.nuevo_sprint', name='nuevo_sprint'),
    url(r'^sprint/(?P<id_sprint>\d+)/muro/$','principal.views.ver_muro', name='ver_muro'),
    url(r'^sprint/(?P<id_sprint>\d+)/graficas/$','principal.views.ver_graficas', name='ver_graficas'),
    url(r'^sprint/(?P<id_sprint>\d+)/reuniones/$','principal.views.ver_reuniones', name='ver_reuniones'),
    url(r'^calendario/(?P<id_proyecto>\d+)$','principal.views.calendario', name='calendario'),
    url(r'^poker/py/(?P<id_proyecto>\d+)$','principal.views.sprints_poker', name='sprints_poker'),
    url(r'^poker/py/(?P<id_proyecto>\d+)/sprint/(?P<id_sprint>\d+)$','principal.views.planning_poker', name='planning_poker'),
    url(r'^poker/py/(?P<id_proyecto>\d+)/sprint/(?P<id_sprint>\d+)/ht/(?P<id_historia>\d+)/v/(?P<voto>\d+)$','principal.views.votar_poker', name='votar_poker'),
    url(r'^elegir/poker/py/(?P<id_proyecto>\d+)/sprint/(?P<id_sprint>\d+)/ht/(?P<id_historia>\d+)/v/(?P<voto>\d+)$','principal.views.elegir_estimacion', name='elegir_estimacion'),
    url(r'^reiniciar/poker/py/(?P<id_proyecto>\d+)/sprint/(?P<id_sprint>\d+)/ht/(?P<id_historia>\d+)$','principal.views.reiniciar_estimacion', name='reiniciar_estimacion'),
    url(r'^/sprint/(?P<id_sprint>\d+)/asignar/tarea/(?P<id_tarea>\d+)$', 'principal.views.asignar_tarea', name='asignar_tarea'),
)

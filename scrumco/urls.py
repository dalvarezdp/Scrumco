from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scrumco.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'principal.views.inicio'),
    #url(r'^privado','principal.views.privado'),
    url(r'^ingresar', 'principal.views.ingresar'),
    url(r'^registro', 'principal.views.registro'),
    url(r'^cerrar','principal.views.cerrar'),
)

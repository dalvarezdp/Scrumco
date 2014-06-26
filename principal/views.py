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
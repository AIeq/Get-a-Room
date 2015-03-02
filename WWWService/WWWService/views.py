from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext as _
from django.core.context_processors import csrf
import re
import urllib2

def search(request):
  context = {}
  context.update(csrf(request))
  context.update({'emptyResults': 1})
  return render(request, "index.html", context) 

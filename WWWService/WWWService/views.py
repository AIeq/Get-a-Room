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
import RoomData

def search(request):
  building = 'Maarintalo'
  email = ''
  time = ''
  
  context = {}
  context.update(csrf(request))
  try:
    email = request.POST.get('email')
    time = request.POST.get('time') 
    context.update({ 'email': email, 'time': time})
    
    # search
    
    if int(time) > 20 and int(time) < 30:
      context.update({"OK": True, 'rooms': RoomData.getRoomData(building)})
    else:
      context.update({"OK": False, 'msg': 'No rooms available.'})
    
  except Exception as e:
    context.update({'emptyResults': 1})
  return render(request, "index.html", context) 

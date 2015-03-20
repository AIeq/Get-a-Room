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
  building = '' 
  
  context = {}
  context.update(csrf(request))
  try:
    building = request.POST.get('building')
  except Exception as e:
    context.update({'building': None})
  try:
    email = request.POST.get('email')
  except Exception as e:
    email = ''
  try:
    time = request.POST.get('time')
    time = int(time) 
  except Exception as e:
    time = 0
  try:
    time2 = request.POST.get('time2')
    time2 = int(time2) 
  except Exception as e:
    time2 = 0
  context.update({'building': building, 'email': email, 'time': time, 'time2': time2})
  context.update({'noBuilding': False})
  
  # search
  
  if time > 20 and time < 30:
    context.update({"OK": True, 'rooms': RoomData.getRoomData(building)})
  else:
    context.update({"OK": False, 'msg': 'No rooms available.'})
  
  return render(request, "index.html", context) 

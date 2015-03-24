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
import ReservationData
import time as tt

def search(request):
  building = '' 
  localtime = tt.localtime()
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
    time = localtime[3];
  try:
    time2 = request.POST.get('time2')
    time2 = int(time2) 
  except Exception as e:
    time2 = localtime[3] + 1;
  try:
    day = request.POST.get('day') 
  except Exception as e:
    day = 'today'
  if day is None:
    day = 'today'
  context.update({'building': building, 'email': email, 'time': time, 'time2': time2, 'day': day})
  context.update({'noBuilding': False})
  
  # no search, always send all data
  roomData = RoomData.getRoomData(building)
  for room in roomData:
    room['reservationData'] = ReservationData.GetReservationData(building, room['id']);
  
  context.update({"OK": True, 'rooms': roomData})
    #context.update({"OK": False, 'msg': 'No rooms available.'})
  
  return render(request, "index.html", context) 

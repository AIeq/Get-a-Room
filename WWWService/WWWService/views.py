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
import datetime
import sys

def flipArray(array):
  return map(list, zip(*array))
  
def clean(array):
  if array[0] == '':
    return[] 
  else:
    return array
    
def search(request, building = None, roomID = None):
  localtime = tt.localtime()
  currentDay = datetime.datetime.now().weekday() # monday=0.. sunday=6
  currentTimeSlot = localtime[3] - 8
  context = {}
  context.update(csrf(request))  
  context.update({'buildings': RoomData.getBuildings()})
  try:
    email = request.POST.get('email')
  except Exception as e:
    email = ''
  if building == None :
    try:
      building = request.POST.get('building')
    except Exception as e:
      "nothing"
  context.update({'building': building})
  if roomID == None :
    try:
      roomID = request.POST.get('roomID')
    except Exception as e:
      "nothing"
  if email != '' and building != None:
    try:
      reserve = request.POST.get('reserve')
    except Exception as e:
      reserve = ''
    try:
      reserve = reserve.split(':')
      roomID = reserve[0]
      times = filter(None, reserve[1].split(' '))
    except Exception as e:
      times = []
    ok = True
    #print >>sys.stderr, times
    reservationTimes =''
    for reservationTime in times:
      day, slot = reservationTime.split(',')
      if ReservationData.ReserveRoom(building, roomID, int(day), int(slot), email):
        reservationTimes += str(int(slot)+8) + '-' +str(int(slot)+9) + ', '
      else: 
        ok = False 
    context.update({'reservationSuccess': ok and len(times) > 0, 'reservationTimes': reservationTimes[:-2]})
    #TODO: handle errors
    roomData = RoomData.getRoomData(building)
    for room in roomData:
      room['reservationData'] = flipArray(ReservationData.GetAnonymizedReservationData(building, room['id'],currentDay,currentTimeSlot,email,'thisWeek') + ReservationData.GetAnonymizedReservationData(building, room['id'],0,0,email,'nextWeek'))
      room['statistics'] = flipArray(ReservationData.GetStatistics(building, room['id']))
    context.update({'rooms': roomData})
  else:
    context.update({'reservationSuccess': False, 'reservationTimes': ''})
    
  context.update({'roomID': roomID})
  try:
    time = request.POST.get('time')
    time = str(int(time)) + ':00'
  except Exception as e:
    time = str(localtime[3]) + ':00';
  try:
    time2 = request.POST.get('time2')
    time2 = str(int(time2)) + ':00'
  except Exception as e:
    time2 = str(localtime[3] + 1) + ':00';
  try:
    day = request.POST.get('day') 
  except Exception as e:
    day = 'today'
  if day is None:
    day = 'today'
  
  context.update({'building': building, 'email': email, 'time': time, 'time2': time2, 'day': day})

  
  #print >>sys.stderr, context
  return render(request, "index.html", context) 

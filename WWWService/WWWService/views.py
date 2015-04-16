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
    for reservationTime in times:
      day, slot = reservationTime.split(',')
      ok = ok and ReservationData.ReserveRoom(building, roomID, int(day), int(slot), email)
    #TODO: handle errors

    roomData = RoomData.getRoomData(building)
    for room in roomData:
      room['reservationData'] = flipArray(ReservationData.GetAnonymizedReservationData(building, room['id'],currentDay,currentTimeSlot,email,'thisWeek') + ReservationData.GetAnonymizedReservationData(building, room['id'],0,0,email,'nextWeek'))
      room['statistics'] = flipArray(ReservationData.GetStatistics(building, room['id']))
    context.update({'rooms': roomData})
  
  context.update({'roomID': roomID})
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

  
  return render(request, "index.html", context) 

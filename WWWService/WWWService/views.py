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
import Emails

def flipArray(array):
  return map(list, zip(*array))
  
def clean(array):
  if array[0] == '':
    return[] 
  else:
    return array
    
def getReservationTimes(times):
  reservationTimes =''
  for reservationTime in times:
    day, slot = reservationTime.split(',')
    reservationTimes += str(int(slot)+8) + '-' +str(int(slot)+9) + ', '
  return reservationTimes[:-2]
  
def reserveTimes(building, roomID, email, times):
  reservationFails =''
  for reservationTime in times:
    day, slot = reservationTime.split(',')
    if not ReservationData.ReserveRoom(building, roomID, int(day), int(slot), email): 
      reservationFails += str(int(slot)+8) + '-' +str(int(slot)+9) + ', '
  return reservationFails[:-2]
  
def search(request, building = None, roomID = None, reserveEmail = None, reserveByEmail = None):
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
  if email != None and building != None:
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
    reservationTimes = getReservationTimes(times)
    ok = True
    #print >>sys.stderr, times
    if len(times) > 1 and not Emails.emailFoundInDatabase(email):
      Emails.sendConfirmationEmail(building, roomID, email, reservationTimes, reserve[1])
      context.update({'reservationPending': True, 'reservationTimes': reservationTimes})
    else:
      reservationFails = reserveTimes(building, roomID, email, times)
      if reservationFails == '':
        context.update({'reservationSuccess': len(times) > 0, 'reservationTimes': reservationTimes})
      else:
        context.update({'reservationFailure': True, 'reservationTimes': reservationFails})
    #TODO: handle errors
  if email == None and reserveByEmail != None: 
    email = reserveEmail
    times = filter(None, reserveByEmail.split('_')) 
    #print >>sys.stderr, times
    reservationFails = reserveTimes(building, roomID, email, times)
    if reservationFails == '':
      context.update({'reservationSuccess': True, 'reservationTimes': getReservationTimes(times)})
    else:
      context.update({'reservationFailure': True, 'reservationTimes': reservationFails})
    #TODO: handle errors
  if building != None:
    roomData = RoomData.getRoomData(building)
    for room in roomData:
      room['reservationData'] = flipArray(ReservationData.GetAnonymizedReservationData(building, room['id'],currentDay,currentTimeSlot,email,'thisWeek') + ReservationData.GetAnonymizedReservationData(building, room['id'],0,0,email,'nextWeek'))
      room['statistics'] = flipArray(ReservationData.GetStatistics(building, room['id']))
    context.update({'rooms': roomData})

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

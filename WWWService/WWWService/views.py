from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext as _
from django.core.context_processors import csrf
from datetime import date, timedelta
import re
import urllib2
import RoomData
import ReservationData
import sys
import Emails
import time as tt

def flipArray(array):
  return map(list, zip(*array))
  
def clean(array):
  if array[0] == '':
    return[] 
  else:
    return array
  
def reserveTimes(building, roomID, email, timeCodes):
  reservationFails =''
  for timeCode in timeCodes:
    day, slot = timeCode.split(',') 
    if not ReservationData.ReserveRoom(building, roomID, int(day), int(slot), email): 
      reservationFails += ReservationData.getReservationTimes([timeCode]) + ', ' 
  return reservationFails[:-2]
  
def cancelTimes(building, roomID, email, timeCodes):
  reservationFails =''
  for timeCode in timeCodes:
    day, slot = timeCode.split(',')
    if not ReservationData.ReleaseRoom(building, roomID, int(day), int(slot), email): 
      reservationFails += ReservationData.getReservationTimes([timeCode]) + ', '
  return reservationFails[:-2]
  
def search(request, building = None, roomID = None, reserveEmail = None, reserveByEmail = None):
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
      
  timeCodes = []
  if email != None and building != None:
    try:
      reserve = request.POST.get('reserve')
    except Exception as e:
      reserve = ''
    try:
      reserve = reserve.split(':')
      roomID = reserve[0]
      timeCodes = filter(None, reserve[1].split(' '))
    except Exception as e:
      timeCodes = []
    if roomID == 'manageReservations':
        roomID = ''
        Emails.sendReservationsEmail(building, email)
        context.update({'manageReservations': True})

    reservationTimes = ReservationData.getReservationTimes(timeCodes)
    ok = True
    #print >>sys.stderr, timeCodes
    if (len(timeCodes) > 1 or len(timeCodes) == 1 and len(ReservationData.findAllReservations(email)) > 0) and not Emails.emailFoundInDatabase(email):
      Emails.sendConfirmationEmail(building, roomID, email, reservationTimes, reserve[1])
      context.update({'reservationPending': True, 'reservationTimes': reservationTimes})
    else:
      reservationFails = reserveTimes(building, roomID, email, timeCodes)
      if reservationFails == '':
        context.update({'reservationSuccess': len(timeCodes) > 0, 'reservationTimes': reservationTimes})
      else:
        context.update({'reservationFailure': True, 'reservationTimes': reservationFails})

    #TODO: handle errors
  if email == None and reserveByEmail != None: 
    email = reserveEmail
    Emails.saveEmail(email)
    if reserveByEmail[0] != 'c':
      timeCodes = filter(None, reserveByEmail.split('_')) 
      #print >>sys.stderr, timeCodes
      reservationFails = reserveTimes(building, roomID, email, timeCodes)
      if reservationFails == '':
        context.update({'reservationSuccess': True, 'reservationTimes': ReservationData.getReservationTimes(timeCodes)})
      else:
        context.update({'reservationFailure': True, 'reservationTimes': reservationFails})
    else:
      timeCodes = filter(None, reserveByEmail[1:].split('_'))
      cancellationFails = cancelTimes(building, roomID, email, timeCodes)
      if cancellationFails == '':
        context.update({'cancellationSuccess': True, 'reservationTimes': ReservationData.getReservationTimes(timeCodes)})
      else:
        context.update({'cancellationFailure': True, 'reservationTimes': cancellationFails})
    #TODO: handle errors
  if building != None:
    roomData = RoomData.getRoomData(building)
    for room in roomData:
      room['reservationData'] = flipArray(ReservationData.GetAnonymizedReservationData(building, room['id'], reserved = timeCodes))
      room['statistics'] = flipArray(ReservationData.GetStatistics(building, room['id']))
    context.update({'rooms': roomData})

  context.update({'roomID': roomID})
  timeNow = tt.localtime()[3]
  try:
    time = request.POST.get('time')
    time = str(int(time)) + ':00'
  except Exception as e:
    time = str(timeNow) + ':00';
  try:
    time2 = request.POST.get('time2')
    time2 = str(int(time2)) + ':00'
  except Exception as e:
    time2 = str(timeNow + 1) + ':00';
  try:
    day = request.POST.get('day') 
  except Exception as e:
    day = 'today'
  if day is None:
    day = 'today'
  #maxday goes until sunday next week
  maxday = str(date.today()+timedelta(days=13-date.weekday(date.today())))
  
  context.update({'building': building, 'email': email, 'time': time, 'time2': time2, 'day': day, 'maxday': maxday})

  
  #print >>sys.stderr, context
  return render(request, "index.html", context) 

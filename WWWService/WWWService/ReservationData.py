#!/usr/bin/python

from copy import deepcopy
import random
from rooms.models import Building
from rooms.models import Room
from rooms.models import Reservation

import sys
def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]
### Populate database ###
slotsInDay = 12
emptyWeekString = ',' * (7*slotsInDay-1)
emptyStatisticWeekString = '0,' * (7*slotsInDay-1) + '0'
def generateDummyStatistics():
  statisticsString = ''
  for d in range(7):
    for t in range(12):
      rushhour1 = 2 + 2 * int(d > 4)
      peak1 = 3-abs(t - rushhour1) / 6.0;
      rushhour2 = 10 - 2 * int(d > 4)
      peak2 = 5-abs(t - rushhour2) / 5.0; 
      peak = max(0.2, peak1, peak2)
      uses = random.uniform(peak*0.6, peak)
      statisticsString += str(int(100*uses)) + ','
  return statisticsString[:-1]
  
def getReservationObject(room):
  try:
    return Reservation.objects.get(room=room)
  except Exception as e:
    res =Reservation(
      room = room,
      lastWeek = emptyWeekString,
      thisWeek = emptyWeekString,
      nextWeek = emptyWeekString,
      statistics = generateDummyStatistics(),
      )
    res.save()
    return res

for room in Room.objects.all():
  getReservationObject(room)    
def GetReservationData(building, roomID):
  "This queries reservation database and returns entries for a room in a building"
  room = Room.objects.get(building=building, roomID = roomID)
  data = DeSerialize(getReservationObject(room))
  #print >>sys.stderr, data
  return data
  
def DeSerialize(res):
  result ={
      'lastWeek' : chunks(res.lastWeek.split(','), slotsInDay),
      'thisWeek' : chunks(res.thisWeek.split(','), slotsInDay),
      'nextWeek' : chunks(res.nextWeek.split(','), slotsInDay),
      'statistics' : chunks(map(int, res.statistics.split(',')), slotsInDay),
  } 
  return result

def SetReservationData(building, roomID, d):
  "This queries reservation database and stores entries for a room in a building"
  room = Room.objects.get(building=building, roomID = roomID)
  res = getReservationObject(room)
  #serialize
  lastWeekString = ''
  thisWeekString = ''
  nextWeekString = ''
  statisticsString = ''
  for nextWeek, thisWeek, lastWeek, statistics in zip(d['nextWeek'], d['thisWeek'], d['lastWeek'], d['statistics']):
    for timeSlot, _ in enumerate(thisWeek):
      lastWeekString += lastWeek[timeSlot] + ','
      thisWeekString += thisWeek[timeSlot] + ','
      nextWeekString += nextWeek[timeSlot] + ','
      statisticsString += str(statistics[timeSlot]) + ','
  res.lastWeek = lastWeekString[:-1]
  res.thisWeek = thisWeekString[:-1]
  res.nextWeek = nextWeekString[:-1]
  res.statistics = statisticsString[:-1]
  res.save();
  
import time as tt
import datetime
def GetAnonymizedReservationData(building, roomID, email):
  "This queries reservation database and returns entries for a room in a building, removes emails" 
  localtime = tt.localtime()
  currentDay = datetime.datetime.now().weekday() # monday=0.. sunday=6
  currentTimeSlot = localtime[3] - 8
  return AnonymizeReservationData(building, roomID, currentDay, currentTimeSlot, email, 'thisWeek') +\
    AnonymizeReservationData(building, roomID, 0, 0, email, 'nextWeek')
    
def AnonymizeReservationData(building, roomID, currentDay, currentTimeSlot, email, week):
  d = GetReservationData(building, roomID)
  #d = buildings['Kirjasto']['112a']
  
  reservations = []
  for day, week in enumerate(d[week]):
    reservations.append([])
    for timeSlot, _ in enumerate(week):
      if week[timeSlot] == '':
        if day < currentDay or day == currentDay and timeSlot < currentTimeSlot:
          reservations[day].append(0)
        else:
          reservations[day].append(1)
      elif week[timeSlot] == email:
        reservations[day].append(2)
      else:
        reservations[day].append(3)
        
  return reservations
def GetStatistics(building, roomID):
  d = GetReservationData(building, roomID)
  statistics = deepcopy(d['statistics'])
  for day, lastWeek in enumerate(d['lastWeek']):
    for timeSlot, _ in enumerate(lastWeek):
      statistics[day][timeSlot] += int(lastWeek[timeSlot] != '')
  return statistics

def ReserveRoom(building, roomID, weekday, timeslot, email):
  return changeEmail(building, roomID, weekday, timeslot, '', email)

def ReleaseRoom(building, roomID, weekday, timeslot, email):
  return changeEmail(building, roomID, weekday, timeslot, email, '')
  
def changeEmail(building, roomID, weekday, timeslot, expectedValue, newValue):
  "Timeslot is 0-12, 0 means from 8 to 9 am"
  if weekday < 7:
    week = 'thisWeek'
  else:
    week = 'nextWeek'
    weekday -= 7
  d = GetReservationData(building, roomID)
  day = d[week][weekday]
  #print >>sys.stderr, day[timeslot]
  #print >>sys.stderr, expectedValue
  #print >>sys.stderr, newValue
  if day[timeslot] == expectedValue:
    day[timeslot] = newValue
    SetReservationData(building, roomID, d)
    return True
  else:
    return False


def EndWeek():
  for room in Room.objects.all():
    d = DeSerialize(getReservationObject(room))
    for nextWeek, thisWeek, lastWeek, statistics in zip(d['nextWeek'], d['thisWeek'], d['lastWeek'], d['statistics']):
      for timeSlot, _ in enumerate(thisWeek):
        statistics[timeSlot] += int(lastWeek[timeSlot] != '')
        lastWeek[timeSlot] = thisWeek[timeSlot]
        thisWeek[timeSlot] = nextWeek[timeSlot]
        nextWeek[timeSlot] = ''
        
def findAllReservations(email):
  reservations = {}
  for building in Building.objects.all():
    rooms ={}
    for room in Room.objects.filter(building=building):
      d = DeSerialize(getReservationObject(room))
      reservationTimes = []
      for day, thisWeek,  in enumerate(d['thisWeek']):
        for timeSlot, _ in enumerate(thisWeek):
          if thisWeek[timeSlot] == email:
            reservationTimes.append(str(day) + ',' + str(timeSlot))
      for day, nextWeek,  in enumerate(d['nextWeek']):
        for timeSlot, _ in enumerate(nextWeek):
          if nextWeek[timeSlot] == email:
            reservationTimes.append(str(day + 7) + ',' + str(timeSlot))    
          
      if len(reservationTimes) > 0:
        rooms[room.roomID] = reservationTimes
    if len(rooms) > 0:
      reservations[building.name] = rooms
  return reservations
  
def getReservationTimes(timeCodes):
  dayNames = [
    'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday',
    'Next weeks Monday','Next weeks Tuesday','Next weeks Wednesday',
    'Next weeks Thursday','Next weeks Friday','Next weeks Saturday','Next weeks Sunday']
  reservationTimes =''
  for timeCode in timeCodes:
    day, slot = timeCode.split(',')
    reservationTimes += dayNames[int(day)] + ' ' + str(int(slot)+8) + '-' +str(int(slot)+9) + ', '
  return reservationTimes[:-2] 
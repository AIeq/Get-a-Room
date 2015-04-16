#!/usr/bin/python

from copy import deepcopy
emptyDay = ['','','','','','','','','','','','',]
emptyWeek = [deepcopy(emptyDay),deepcopy(emptyDay),deepcopy(emptyDay),
    deepcopy(emptyDay),deepcopy(emptyDay),deepcopy(emptyDay),deepcopy(emptyDay),]
emptyRoom = {'nextWeek': deepcopy(emptyWeek),
    'thisWeek': deepcopy(emptyWeek),
    'lastWeek': deepcopy(emptyWeek),
    'statistics': [
    [0,0,0,0,0,0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,0,0,0,0,],],}
dummyRoom = {'nextWeek': [
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','hello@aalto.fi','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],],
    'thisWeek': [
    ['','','','','','','','','','hello@aalto.fi','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],['','','','','hello@aalto.fi','','','','','','','',],
    ['','','','','','','','','','','','',],],
    'lastWeek': deepcopy(emptyWeek),
    'statistics': [
    [0,1,2,2,1,0,0,0,0,1,1,0,],[0,1,0,0,2,3,3,0,0,0,2,0,],
    [0,0,4,4,0,0,1,0,0,2,2,0,],[0,0,1,2,0,2,0,3,0,0,2,0,],
    [0,0,0,3,3,0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,1,3,3,2,0,],
    [0,0,0,0,0,0,0,0,1,1,0,0,],],}
 
data1 = {
  '112a':deepcopy(emptyRoom),
  '112b':deepcopy(dummyRoom),
  '243a':deepcopy(emptyRoom),
  '243b':deepcopy(emptyRoom),
  }
  
data2 = {
  '142a':deepcopy(emptyRoom),
  '142b':deepcopy(dummyRoom),
  '143a':deepcopy(emptyRoom),
  '143b':deepcopy(emptyRoom),
  '243a':deepcopy(emptyRoom),
  '243b':deepcopy(emptyRoom),
  }

buildings = {'Kirjasto': data1, 'Maarintalo': data2}

from rooms.models import Room
from rooms.models import Reservation
import sys
def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]
### Populate database ###
emptyWeekString = ',' * (7*8-1)
emptyStatisticWeekString = '0,' * (7*8-1) + '0'
if Reservation.objects.all().count() == 0:
  for room in Room.objects.all():
    Reservation(
      room = room,
      lastWeek = emptyWeekString,
      thisWeek = emptyWeekString,
      nextWeek = emptyWeekString,
      statistics = emptyStatisticWeekString,
      ).save()
  
def GetReservationData(building, roomID):
  "This queries reservation database and returns entries for a room in a building"
  room = Room.objects.get(building=building, roomID = roomID)
  res = Reservation.objects.get(room=room)
  #print >>sys.stderr, DeSerialize(res)
  return DeSerialize(res)
  #return buildings[building][roomID]# this version will just return static list
  
def DeSerialize(res):
  result ={
      'lastWeek' : chunks(res.lastWeek.split(','), 8),
      'thisWeek' : chunks(res.thisWeek.split(','), 8),
      'nextWeek' : chunks(res.nextWeek.split(','), 8),
      'statistics' : chunks(map(int, res.statistics.split(',')), 8),
  } 
  return result

def SetReservationData(building, roomID, d):
  "This queries reservation database and stores entries for a room in a building"
  room = Room.objects.get(building=building, roomID = roomID)
  res = Reservation.objects.get(room=room)
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

def GetAnonymizedReservationData(building, roomID, currenDay, currentTimeSlot, email, week):
  "This queries reservation database and returns entries for a room in a building, removes emails"
  d = GetReservationData(building, roomID)
  #d = buildings['Kirjasto']['112a']
  
  reservations = []
  for day, week in enumerate(d[week]):
    reservations.append([])
    for timeSlot, _ in enumerate(week):
      if day < currenDay or day == currenDay and timeSlot < currentTimeSlot:
        reservations[day].append(0)
      elif week[timeSlot] == '':
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
  "Timeslot is 0-12, 0 means from 8 to 9 am"
  if weekday < 7:
    week = 'thisWeek'
  else:
    week = 'nextWeek'
    weekday -= 7
  d = GetReservationData(building, roomID)
  day = d[week][weekday]
  if day[timeslot] == '':
    day[timeslot] = email
    SetReservationData(building, roomID, d)
    return True
  else:
    return False

def ReleaseRoom(building, roomID, weekday, timeslot):
  "Timeslot is 0-12, 0 means from 8 to 9 am"
  if weekday < 7:
    week = 'thisWeek'
  else:
    week = 'nextWeek'
    weekday -= 7
  d = GetReservationData(building, roomID)
  d[week][weekday][timeslot] = ''
  SetReservationData(building, roomID, d)


def EndWeek():
  for room in Room.objects.all():
    res = Reservation.objects.get(room=room)
    d = DeSerialize(res)
    for nextWeek, thisWeek, lastWeek, statistics in zip(d['nextWeek'], d['thisWeek'], d['lastWeek'], d['statistics']):
      for timeSlot, _ in enumerate(thisWeek):
        statistics[timeSlot] += int(lastWeek[timeSlot] != '')
        lastWeek[timeSlot] = thisWeek[timeSlot]
        thisWeek[timeSlot] = nextWeek[timeSlot]
        nextWeek[timeSlot] = ''
  
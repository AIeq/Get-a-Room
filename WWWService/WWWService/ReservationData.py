#!/usr/bin/python

from copy import deepcopy

emptyRoom = {'nextWeek': [
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],],
    'thisWeek': [
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],],
    'lastWeek': [
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],['','','','','','','','','','','','',],
    ['','','','','','','','','','','','',],],
    'statistics': [
    [0,0,0,0,0,0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,0,0,0,0,],[0,0,0,0,0,0,0,0,0,0,0,0,],
    [0,0,0,0,0,0,0,0,0,0,0,0,],],}
 
data1 = {
  '112a':deepcopy(emptyRoom),
  '112b':deepcopy(emptyRoom),
  '243a':deepcopy(emptyRoom),
  '243b':deepcopy(emptyRoom),
  }
  
data2 = {
  '142a':deepcopy(emptyRoom),
  '142b':deepcopy(emptyRoom),
  '143a':deepcopy(emptyRoom),
  '143b':deepcopy(emptyRoom),
  '243a':deepcopy(emptyRoom),
  '243b':deepcopy(emptyRoom),
  }

buildings = {'Kirjasto': data1, 'Maarintalo': data2}

def GetReservationData(building, room):
  "This queries reservation database and returns entries for a room in a building"
  "The first version will just return static list"
  return buildings[building][room]['thisWeek']
  
def GetStatistics(building, room):
  d = buildings[building][room]
  statistics = deepcopy(d['statistics'])
  for lastWeek in d['lastWeek']:
    for timeSlot, _ in enumerate(lastWeek):
      statistics[timeSlot] += int(lastWeek[timeSlot] != '')
  return statistics

def ReserveRoom(building, room, weekday, timeslot, email):
  "Timeslot is 0-12, 0 means from 8 to 9 am"
  day = buildings[building][room]['thisWeek'][weekday]
  if day[timeslot] == '':
    day[timeslot] = email
    return True
  else:
    return False

def ReleaseRoom(building, room, weekday, timeslot):
  "Timeslot is 0-12, 0 means from 8 to 9 am"
  buildings[building][room]['thisWeek'][weekday][timeslot] = ''
  
def ReserveRoomAdvance(building, room, weekday, timeslot, email):
  "Timeslot is 0-12, 0 means from 8 to 9 am"
  day = buildings[building][room]['nextWeek'][weekday]
  if day[timeslot] == '':
    day[timeslot] = email
    return True
  else:
    return False

def ReleaseRoomAdvance(building, room, weekday, timeslot):
  "Timeslot is 0-12, 0 means from 8 to 9 am"
  buildings[building][room]['nextWeek'][weekday][timeslot] = ''

def EndWeek(building):
    for roomName, d in buildings[building].iteritems():
        for nextWeek, thisWeek, lastWeek, statistics in zip(d['nextWeek'], d['thisWeek'], d['lastWeek'], d['statistics']):
            for timeSlot, _ in enumerate(thisWeek):
                statistics[timeSlot] += int(lastWeek[timeSlot] != '')
                lastWeek[timeSlot] = thisWeek[timeSlot]
                thisWeek[timeSlot] = nextWeek[timeSlot]
                nextWeek[timeSlot] = ''
  
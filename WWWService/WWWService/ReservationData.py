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

def GetReservationData(building, room):
  "This queries reservation database and returns entries for a room in a building"
  "The first version will just return static list"
  return buildings[building][room]['thisWeek']

def GetAnonymizedReservationData(building, room, currenDay, currentTimeSlot, email):
  "This queries reservation database and returns entries for a room in a building"
  "The first version will just return static list"
  
  #print buildings['Kirjasto']['112a']

  d = buildings[building][room]
  #d = buildings['Kirjasto']['112a']
  
  reservations = []
  for day, thisWeek in enumerate(d['thisWeek']):
    reservations.append([])
    for timeSlot, _ in enumerate(thisWeek):
      if day < currenDay or day == currenDay and timeSlot < currentTimeSlot:
        reservations[day].append(0)
      elif thisWeek[timeSlot] == '':
        reservations[day].append(1)
      elif thisWeek[timeSlot] == email:
        reservations[day].append(2)
      else:
        reservations[day].append(3)
        
  return reservations
  
def GetStatistics(building, room):
  d = buildings[building][room]
  statistics = deepcopy(d['statistics'])
  for day, lastWeek in enumerate(d['lastWeek']):
    for timeSlot, _ in enumerate(lastWeek):
      statistics[day][timeSlot] += int(lastWeek[timeSlot] != '')
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
  
#!/usr/bin/python

from copy import deepcopy

emptyWeek = {'thisWeek': [
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
 
data = {
  '142a':deepcopy(emptyWeek),
  '142b':deepcopy(emptyWeek),
  '143a':deepcopy(emptyWeek),
  '143b':deepcopy(emptyWeek),
  '243a':deepcopy(emptyWeek),
  '243b':deepcopy(emptyWeek),
  }

buildings = {'': deepcopy(data), 'Kirjasto': deepcopy(data), 'Maarintalo': deepcopy(data)}

def GetReservationData(building, room):
  "This queries reservation database and returns entries for a room in a building"
  "The first version will just return static list"
  return buildings[building][room]

def ReserveRoom(building, room, day, timeslot, email):
  "Timeslot is 0-12, 0 means from 8 to 9 am"
  buildings[building][room]['thisWeek'][day][timeslot] = email

def EndWeek(building):
    for roomName, d in buildings[building].iteritems():
        for thisWeek, lastWeek, statistics in zip(d['thisWeek'], d['lastWeek'], d['statistics']):
            for timeSlot, _ in enumerate(thisWeek):
                statistics[timeSlot] += int(lastWeek[timeSlot] != '')
                lastWeek[timeSlot] = thisWeek[timeSlot]
                thisWeek[timeSlot] = ''
  
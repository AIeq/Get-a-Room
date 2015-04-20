#!/usr/bin/python
 

data1 = [
  {'id': '112a', 'location': 'first floor', 'size': 6, 'type': 'meeting room', 'features': ['Two tables', 'Projector'], 'insights': [], 'picture': '112a.jpg'}, 
  {'id': '112b', 'location': 'first floor', 'size': 6, 'type': 'meeting room', 'features': ['Two tables', 'Projector'], 'insights': [], 'picture': '112b.jpg'}, 
  {'id': '243a', 'location': 'second floor', 'size': 4, 'type': 'work room', 'features': ['table'], 'insights': [], 'picture': '243a.jpg'}, 
  {'id': '243b', 'location': 'second floor', 'size': 4, 'type': 'work room', 'features': ['table'], 'insights': [], 'picture': '243b.jpg'},
  ]
   
data2 = [
  {'id': '142a', 'location': 'first floor', 'size': 6, 'type': 'meeting room', 'features': ['Two tables', 'Projector'], 'insights': [], 'picture': '142a.jpg'}, 
  {'id': '142b', 'location': 'first floor', 'size': 6, 'type': 'meeting room', 'features': ['Two tables', 'Projector'], 'insights': [], 'picture': '142b.jpg'}, 
  {'id': '143a', 'location': 'first floor', 'size': 4, 'type': 'work room', 'features': ['table', 'Projector'], 'insights': [], 'picture': '143a.jpg'}, 
  {'id': '143b', 'location': 'first floor', 'size': 4, 'type': 'work room', 'features': ['table'], 'insights': [], 'picture': '143b.jpg'},
  {'id': '243a', 'location': 'second floor', 'size': 4, 'type': 'work room', 'features': ['table'], 'insights': [], 'picture': '243a.jpg'}, 
  {'id': '243b', 'location': 'second floor', 'size': 4, 'type': 'work room', 'features': ['table'], 'insights': [], 'picture': '243b.jpg'},
  ]
buildings = {'Kirjasto': data1, 'Maarintalo': data2}

from rooms.models import Building
from rooms.models import Room
import sys

### Populate database ###
if Building.objects.all().count() == 0:
  k = Building(name='Kirjasto', description='Aalto main library')
  k.save()
  Room(building = k, roomID = '112a',location = 'first floor',size = 6,type = 'meeting room',features = 'Two tables, Projector',insights = '',picture = '112a.jpg',).save()
  Room(building = k, roomID = '112b',location = 'first floor',size = 6,type = 'meeting room',features = 'Two tables, Projector',insights = '',picture = '112b.jpg',).save()
  Room(building = k, roomID = '243a',location = 'second floor',size = 4,type = 'work room',features = 'table',insights = '',picture = '243a.jpg',).save()
  Room(building = k, roomID = '243b',location = 'second floor',size = 4,type = 'work room',features = 'table',insights = '',picture = '243b.jpg',).save()
  
  m = Building(name='Maarintalo', description='Utility house')
  m.save()
  Room(building = m, roomID = '142a',location = 'second floor',size = 6,type = 'meeting room',features = 'Two tables, Projector',insights = '',picture = '142a.jpg',).save()
  Room(building = m, roomID = '142b',location = 'second floor',size = 6,type = 'meeting room',features = 'Two tables, Projector',insights = '',picture = '142b.jpg',).save()
  Room(building = m, roomID = '143a',location = 'second floor',size = 4,type = 'work room',features = 'table',insights = '',picture = '143a.jpg',).save()
  Room(building = m, roomID = '143b',location = 'second floor',size = 4,type = 'work room',features = 'table',insights = '',picture = '143b.jpg',).save()
  Room(building = m, roomID = '243a',location = 'second floor',size = 4,type = 'work room',features = 'table',insights = '',picture = '243a.jpg',).save()
  Room(building = m, roomID = '243b',location = 'second floor',size = 4,type = 'work room',features = 'table',insights = '',picture = '243b.jpg',).save()

def getBuildings():
  result = []
  for b in Building.objects.all():
    r = {'name': b.name, 'description': b.description}
    result += [r]
  return result
  
def getRoomData(building):
  "This queries room database and returns entries for all rooms in a building"  
  result = []
  for room in Room.objects.filter(building=building):
    r = {'id': room.roomID, 'location': room.location, 'size': room.size, 'type': room.type,
    'features': filter(None, room.features.split(',')), 'insights': filter(None, room.insights.split(',')), 'picture': room.picture}
    #print >>sys.stderr, r
    result += [r]
  return result
  #return buildings[building] #this version will just return static list

#!/usr/bin/python


data = [
  {'id': '142a', 'location': 'first floor', 'size': 6, 'type': 'meeting room', 'featrures': ['Two tables', 'Projector'], 'insights': [], 'picture': '142a.jpg'}, 
  {'id': '142b', 'location': 'first floor', 'size': 6, 'type': 'meeting room', 'featrures': ['Two tables', 'Projector'], 'insights': [], 'picture': '142b.jpg'}, 
  {'id': '143a', 'location': 'first floor', 'size': 4, 'type': 'work room', 'featrures': ['table'], 'insights': [], 'picture': '143a.jpg'}, 
  {'id': '143b', 'location': 'first floor', 'size': 4, 'type': 'work room', 'featrures': ['table'], 'insights': [], 'picture': '143b.jpg'},
  {'id': '243a', 'location': 'second floor', 'size': 4, 'type': 'work room', 'featrures': ['table'], 'insights': [], 'picture': '243a.jpg'}, 
  {'id': '243b', 'location': 'second floor', 'size': 4, 'type': 'work room', 'featrures': ['table'], 'insights': [], 'picture': '243b.jpg'},
  ]
  

def getRoomData(building):
  "This queries room database and returns entries for all rooms in a building"
  "The first version will just return static list"
  return data

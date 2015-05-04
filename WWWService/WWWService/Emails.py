#!/usr/bin/python
from django.core.mail import EmailMessage
from rooms.models import Email
import ReservationData
import sys

serverAddress = 'http://localhost:8000'

def emailFoundInDatabase(email):
  try:
    Email.objects.get(email=email)
    return True
  except Exception as e:
    Email(email=email).save()
    return False
def createLink(building, roomID, email, timeCodes, msg):
  url =  serverAddress + '/' + building + '/' + roomID + '/' + email + '/' + timeCodes.replace(' ','_')
  return '<a href=" ' + url +'">' + msg + '</a>'
def sendConfirmationEmail(building, roomID, email, reservationTimes, timeCodes):
  msg = 'Click this link to confirm registration for these hours:' + reservationTimes + '<br/>' + \
    createLink(building, roomID, email, timeCodes, 'Confirm')
  mail = EmailMessage('Confirmation of room reservation', '<html><body>' + msg + '</body></html>', to = [email] )
  mail.send()

def sendReservationsEmail(building, email):
  emailFoundInDatabase(email)
  reservations = ReservationData.findAllReservations(email)
  if len(reservations) > 0:
    msg = 'Click these links to manage your registrations:<br/>' + createLinks(reservations, email)
  else:
    msg = 'You do not have any active reservations'
  #print >>sys.stderr, msg
  mail = EmailMessage('Manage reservations', '<html><body>' + msg + '</body></html>', to = [email] )
  mail.content_subtype = "html" 
  mail.send()

  
def createLinks(reservations, email):
  links = ''
  for building, r in reservations.iteritems():
    links += 'Your registrations for ' + building + ':<br/>'
    for roomID, reservationTimes in r.iteritems():
      for timeCode in reservationTimes:
        links += ' ' + roomID + ' ' + ReservationData.getReservationTimes([timeCode]) + \
          ' ' + createLink(building, roomID, email, 'c' + timeCode, 'Cancel') + \
          ' ' + createLink(building, roomID, email, 'r' + timeCode, 'Copy reservation to next week') + '<br/>'
  return links




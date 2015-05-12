#!/usr/bin/python
from django.core.mail import EmailMessage
from rooms.models import Email
import ReservationData
import serverAddress
import sys

emailHeader = \
  '<html><body>' + \
  '&nbsp;&nbsp;<b>Get-a-Room</b><br/>' + \
  '<br/>'
emailFooter = \
  '<br/>' + \
  '<br/>' + \
  'This is an automatically generated email, no need to respond.<br/>' + \
  '2015 (c) Get-a-Room team' + \
  '</body></html>'
def emailFoundInDatabase(email):
  try:
    Email.objects.get(email=email)
    return True
  except Exception as e:
    return False
def saveEmail(email):
    Email(email=email).save()
def createLink(building, roomID, email, timeCodes, msg):
  url =  serverAddress + '/' + building + '/' + roomID + '/' + email + '/' + timeCodes.replace(' ','_')
  return '<a href=" ' + url +'">' + msg + '</a>'
def sendConfirmationEmail(building, roomID, email, reservationTimes, timeCodes):
  msg = 'Click this link to confirm registration for these hours:' + reservationTimes + '<br/>' + \
    createLink(building, roomID, email, timeCodes, 'Confirm')
  mail = EmailMessage('Confirmation of room reservation', emailHeader + msg + emailFooter, to = [email] )
  mail.content_subtype = "html" 
  mail.send()

def sendReservationsEmail(building, email):
  reservations = ReservationData.findAllReservations(email)
  if len(reservations) > 0:
    msg = 'Click these links to manage your registrations:<br/>' + createLinks(reservations, email)
  else:
    msg = 'You do not have any active reservations'
  #print >>sys.stderr, msg
  mail = EmailMessage('Manage reservations', emailHeader + msg + emailFooter, to = [email] )
  mail.content_subtype = "html" 
  mail.send()

def createLinks(reservations, email):
  links = ''
  for building, r in reservations.iteritems():
    links += 'Your registrations for ' + building + ':<br/>'
    for roomID, timeCodes in r.iteritems():
      for timeCode in timeCodes:
        links += '&nbsp;' + roomID + ' ' + ReservationData.getReservationTimes([timeCode])
        links += ' ' + createLink(building, roomID, email, 'c' + timeCode, 'Cancel')
        timeCode = getNextWeekTimeCodes([timeCode])
        if len(timeCode) == 1:
          links += ' ' + createLink(building, roomID, email, timeCode[0], 'Copy reservation to next week')
        links += '<br/>'
      links += ' ' + createLink(building, roomID, email, 'c' + '_'.join(timeCodes), 'Cancel all')
      timeCodes = getNextWeekTimeCodes(timeCodes)
      if timeCodes != None:
        links += ' ' + createLink(building, roomID, email, '_'.join(timeCodes), 'Copy all')
      links += '<br/>'
  return links
def getNextWeekTimeCodes(timeCodes):
  newCodes = []
  for timeCode in timeCodes:
    day, slot = timeCode.split(',')
    if int(day) < 7:
      newCodes.append(str(int(day) + 7) + ',' + slot) 
  return newCodes

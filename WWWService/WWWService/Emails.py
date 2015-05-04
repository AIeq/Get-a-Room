#!/usr/bin/python
from django.core.mail import EmailMessage
from rooms.models import Room
from rooms.models import Reservation
from rooms.models import Email
import sys

serverAddress = 'http://localhost:8000'

def emailFoundInDatabase(email):
  try:
    Email.objects.get(email=email)
    return True
  except Exception as e:
    Email(email=email).save()
    return False
    
def sendConfirmationEmail(building, roomID, email, reservationTimes, timeCodes):
  mail = EmailMessage('Confirmation of room reservation',
    'Click this link to confirm registration for these hours:' + reservationTimes + '\n'
    + serverAddress + '/' + building + '/' + roomID + '/' + email + '/' + timeCodes.replace(' ','_'), to = [email] )
  mail.send()

def sendReservationsEmail(building, email):
  mail = EmailMessage('Manage reservations',
    'Click these links to manage your registrations:' , to = [email] )
  mail.send()

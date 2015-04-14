from django.db import models
from django.contrib import admin 

class Room(models.Model):
    roomID = models.CharField(max_length=200, primary_key=True)
    location = models.CharField(max_length=200)
    size = models.IntegerField()
    type = models.CharField(max_length=200)
    features = models.CharField(max_length=200, blank=True)
    insights = models.CharField(max_length=200, blank=True)
    picture = models.CharField(max_length=200, blank=True)
    def __unicode__(self):
       return 'Room: ' + self.roomID
    
class Email(models.Model):
    email = models.CharField(max_length=200, primary_key=True)
    def __unicode__(self):
       return 'Email: ' + self.email

class Reservation(models.Model):
    room = models.ForeignKey(Room, primary_key=True)
    lastWeek = models.CharField(max_length=200)
    thisWeek = models.CharField(max_length=200)
    nextWeek = models.CharField(max_length=200)
    statistics = models.CharField(max_length=200)
    def __unicode__(self):
       return 'Reservation: ' + self.room.roomID
    
    


admin.site.register(Room)
admin.site.register(Email)
admin.site.register(Reservation)
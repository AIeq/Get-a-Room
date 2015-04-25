from django.db import models
from django.contrib import admin 


class Building(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    description = models.CharField(max_length=200, blank=True)
    def __unicode__(self):
       return 'Building: ' + self.name
       
class Room(models.Model):
    building = models.ForeignKey(Building)
    roomID = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    size = models.IntegerField()
    type = models.CharField(max_length=200)
    features = models.CharField(max_length=200, blank=True)
    insights = models.CharField(max_length=200, blank=True)
    picture = models.CharField(max_length=200, blank=True)
    map = models.CharField(max_length=200, blank=True)
    class Meta:
        unique_together = (("building", "roomID"),)
    def __unicode__(self):
       return 'Room: ' + self.building.name + " " + self.roomID
    
class Email(models.Model):
    email = models.CharField(max_length=200, primary_key=True)
    def __unicode__(self):
       return 'Email: ' + self.email

class Reservation(models.Model):
    room = models.ForeignKey(Room, primary_key=True)
    lastWeek = models.CharField(max_length=924) # 7 * 12 * (10 + 1)
    thisWeek = models.CharField(max_length=924)
    nextWeek = models.CharField(max_length=924)
    statistics = models.CharField(max_length=924)
    def __unicode__(self):
       return 'Reservation: ' + self.room.building.name + " " + self.room.roomID
    
    

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Email)
admin.site.register(Reservation)


from django.db import models

# Create your models here.


class Rooms(models.Model):
    Date =  models.DateField()
    startTime =  models.TimeField()
    endTime = models.TimeField()
    Number = models.IntegerField()


class User(models.Model):
    loginid = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    contact_number = models.IntegerField()
    bookings = models.BooleanField(default = False)

class Admin(models.Model):
    loginid = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    contact_number = models.IntegerField()

from django.db import models

# Create your models here.


class Rooms(models.Model):
    Date =  models.DateField()
    startTime =  models.TimeField()
    endTime = models.TimeField()
    Number = models.IntegerField()
    managerId = models.CharField(max_length=20)

class Bookings(models.Model):
    number = models.IntegerField()
    userid = models.IntegerField()
    managerid = models.IntegerField()
    slot = models.CharField(max_length=20)


class User(models.Model):
    loginid = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    contact_number = models.IntegerField()
    bookings = models.BooleanField(default = False)

class Manager(models.Model):
    loginid = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    contact_number = models.IntegerField()

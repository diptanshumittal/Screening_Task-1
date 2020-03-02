from django.db import models

# Create your models here.


class Rooms(models.Model):
    date =  models.DateField()
    startTime =  models.IntegerField()
    endTime = models.IntegerField()
    rn = models.IntegerField()
    mid = models.IntegerField()
    addate = models.DateField()
    status = models.BooleanField(default = False)

class Bookings(models.Model):
    rid = models.IntegerField()
    cid = models.IntegerField()
    mid = models.IntegerField()


class Customer(models.Model):
    loginid = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 254)

class Manager(models.Model):
    loginid = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 254)

from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Station(models.Model):
    station_name = models.CharField(max_length=20, null=False, default="")

    def __str__(self):
        return self.station_name

    def number_of_bikes(self):
        return self.bike_set.count()


class Bike(models.Model):

    bikeid = models.CharField(max_length=10, default="")
    in_use = models.BooleanField(default=False)
    is_faulty = models.BooleanField(default=False)
    stationid = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Bike ID: {}\nUsage: {}\nCondition: {}\nCurrent Location: {}".format(self.bikeid, self.current_usage, self.condition, self.stationid)

    def current_usage(self):
        if self.in_use:
            return "In Use"
        else:
            return "Free"

    def condition(self):
        if self.is_faulty:
            return "faulty"
        else:
            return "Good"


class Order(models.Model):

    orderid = models.CharField(max_length=10, null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    bikeid = models.ForeignKey(Bike, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(default=timezone.now)
    due_amount = models.FloatField(default=0.00)

    def __str__(self):
        return "Order ID: {}\nCustomer ID: {}\nBike ID: {} ".format(self.orderid, self.customerid, self.bikeid)

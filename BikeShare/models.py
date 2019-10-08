from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
# Create your models here.


class Station(models.Model):
    station_name = models.CharField(max_length=100, null=False, default="")

    def __str__(self):
        return self.station_name

    def number_of_bikes(self):
        available_bikes = self.bike_set.all().filter(in_use=False, is_faulty=False)
        return available_bikes.count()


class Bike(models.Model):

    in_use = models.BooleanField(default=False)
    is_faulty = models.BooleanField(default=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, default="")

    class Meta:
        verbose_name_plural = 'Bikes'

    def current_usage(self):
        if self.in_use:
            return "In Use"
        else:
            return "Free"

    def condition(self):
        if self.is_faulty:
            return "Faulty"
        else:
            return "Good"


class Order(models.Model):

    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    start_station = models.ForeignKey(Station, on_delete=models.CASCADE, default="")
    start_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(default=timezone.now)
    due_amount = models.FloatField(default=0.00)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return "Order ID: {}\nCustomer ID: {}\nBike ID: {} ".format(self.pk, self.user, self.bike)



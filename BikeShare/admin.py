from django.contrib import admin
from .models import Bike, Station, Order
from account.models import Account

# Register your models here.
admin.site.register(Account)
admin.site.register(Bike)
admin.site.register(Station)
admin.site.register(Order)

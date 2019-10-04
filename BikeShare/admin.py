from django.contrib import admin
from .models import Bike, Station, Order, FaultyBikes, PreviousOrders

# Register your models here.

admin.site.register(Bike)
admin.site.register(Station)
admin.site.register(Order)
admin.site.register(FaultyBikes)
admin.site.register(PreviousOrders)
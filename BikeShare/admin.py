from django.contrib import admin
from .models import Bike, Station, Order

# Register your models here.

admin.site.register(Bike)
admin.site.register(Station)
admin.site.register(Order)

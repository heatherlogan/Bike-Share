from django.shortcuts import render, get_object_or_404
from .models import Bike, Station, Order, User, FaultyBikes, PreviousOrders
import datetime

from django.template import loader
# Create your views here.

def home(request):
    return render(request, 'home.html')

def customer_page(request):

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    all_orders = Order.objects.all()
    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'all_orders':all_orders
    }
    return render(request, 'customer_page.html', context=context)


def rent_bike(request, station_id):

    # create new order with customer id, bike id, station id, start time.

    station = get_object_or_404(Station, pk=station_id)
    bike = station.bike_set.first()
    rented_bike = get_object_or_404(Bike, pk=bike.id)
    user_id = get_object_or_404(User, pk= request.POST.get('user_id', False))
    time = datetime.datetime.now()

    new_order = Order(bike=rented_bike, user=user_id, start_station=station, start_time=time)
    new_order.save()

    bike.in_use = True
    bike.save()

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    all_orders = Order.objects.all()
    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'all_orders':all_orders
    }
    return render(request, 'customer_page.html', context=context)


def return_bike(request, order_id):

    order = get_object_or_404(Order, pk=order_id)

    # update order table with end_station_id, end time
    start_time = order.start_time
    end = datetime.datetime.now()



    order.check_out_time = end
    order.due_amount = 100 # TODO change
    order.save()
    bike = get_object_or_404(Bike, pk=order.bike.pk)
    bike.in_use = False
    bike.save()

    # add order to previous orders
    prev_order = PreviousOrders(order.id)
    prev_order.save()

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    all_orders = Order.objects.all()
    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'all_orders':all_orders
    }
    return render(request, 'customer_page.html', context=context)


def report_faulty(request, order_id):

    order = get_object_or_404(Order, pk=order_id)
    bike = order.bike
    bike.is_faulty = True
    faultybike = FaultyBikes(bike.id)
    faultybike.save()

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    all_orders = Order.objects.all()
    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'all_orders':all_orders
    }

    return render(request, 'customer_page.html', context=context)




def operator_page(request):

    faultybikes = FaultyBikes.objects.all()

    return render(request, 'operator_page.html', context={'faulty_bikes':faultybikes})



def manager_page(request):

    all_orders = Order.objects.all()





    return render(request, 'manager_page.html')

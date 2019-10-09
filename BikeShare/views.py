from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Bike, Station, Order, User
from account.models import Account
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import datetime
from .forms import TopUpForm
from django.db.models import Q

from django.template import loader
# Create your views here.

def home(request):
    return render(request, 'home.html')


def customer_page(request):

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    current_orders = Order.objects.all().filter(is_complete=False)
    previous_orders = Order.objects.all().filter(is_complete=True)

    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'current_orders': current_orders,
        'previous_orders' : previous_orders}
    return render(request, 'customer_page.html', context=context)


def rent_bike(request, station_id):

    # create new order with customer id, bike id, station id, start time.

    station = get_object_or_404(Station, pk=station_id)
    bike = station.bike_set.all().filter(in_use=False, is_faulty=False).first()
    rented_bike = get_object_or_404(Bike, pk=bike.id)
    user = get_object_or_404(Account, pk= request.POST.get('user_id', False))

    time = datetime.datetime.now()

    user.hire_in_progress = True
    user.save()

    new_order = Order(bike=rented_bike, user=user, start_station=station, start_time=time)
    new_order.save()

    bike.in_use = True
    bike.save()

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    current_orders = Order.objects.all().filter(is_complete=False)
    previous_orders = Order.objects.all().filter(is_complete=True)
    context = {
        'user':user,
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'current_orders':current_orders,
        'previous_orders':previous_orders
    }
    return render(request, 'customer_page.html', context=context)


def return_bike(request, order_id):

    def calculate_cost(starttime, endtime):
        if starttime.date() == endtime.date():
            hours_used = endtime.hour - starttime.hour
            cost = (hours_used + 1) * 2.00
        else:
            cost = 20.0 * (endtime.day - starttime.day)
        return cost

    order = get_object_or_404(Order, pk=order_id)

    # update order table with end_station_id, end time
    start_time = order.start_time
    end = datetime.datetime.now()

    order.check_out_time = end
    order.due_amount = calculate_cost(start_time, end)
    userid = order.user
    print(userid.pk)
    user = get_object_or_404(Account, pk=userid.pk)
    user.hire_in_progress = False
    user.save()

    bike = get_object_or_404(Bike, pk=order.bike.pk)
    bike.in_use = False
    bike.save()

    order.save()

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    current_orders = Order.objects.all().filter(is_complete=False)
    previous_orders = Order.objects.all().filter(is_complete=True)

    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'current_orders': current_orders,
        'previous_orders' : previous_orders
    }
    return render(request, 'customer_page.html', context=context)



def top_up_balance(request):
    form = TopUpForm()
    return render(request, 'top_up.html', {'form':form})


def submit_top_up(request):
    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            user = request.user
            user.wallet_balance += int(form.cleaned_data['money'])
            user.save()
            print(user.wallet_balance)
            return HttpResponseRedirect(request.POST.get('next', '/'))
    else:
        form = TopUpForm()
    return render(request, 'top_up.html', {'form': form})



def pay_bill(request, order_id):

    # if wallet balance is greater than bill then pay bill
    # else display error message to prompt wallet top up

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    all_orders = Order.objects.all()
    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'all_orders': all_orders
    }

    return render(request, 'customer_page.html', context=context)



def report_faulty(request, order_id):

    order = get_object_or_404(Order, pk=order_id)
    bike = order.bike
    bike.is_faulty = True

    bike.save()

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    current_orders = Order.objects.all().filter(is_complete=False)
    previous_orders = Order.objects.all().filter(is_complete=True)
    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'current_orders': current_orders,
        'previous_orders' : previous_orders}
    return render(request, 'customer_page.html', context=context)



def operator_page(request):

    faultybikes = Bike.objects.all().filter(is_faulty=True)
    free_bikes = Bike.objects.all().filter(in_use=False)
    move_stations = Station.objects.all()

    context = {
        'faulty_bikes': faultybikes,
        'free_bikes': free_bikes,
        'move_stations': move_stations}

    return render(request, 'operator_page.html', context=context)

def repair_bike(request, bike_id):

    bike = get_object_or_404(Bike, pk=bike_id)
    bike.is_faulty = False
    bike.save()

    faultybikes = Bike.objects.all().filter(is_faulty=True)
    free_bikes = Bike.objects.all().filter(in_use=False)
    move_stations = Station.objects.all().filter(~Q(station_name=bike.station.station_name))

    context = {
        'faulty_bikes': faultybikes,
        'free_bikes': free_bikes,
        'move_stations': move_stations}

    return render(request, 'operator_page.html', context=context)
    return render(request, 'operator_page.html', context=context)


def move_bike(request, bike_id):
    bike = get_object_or_404(Bike, pk=bike_id)

    faultybikes = Bike.objects.all().filter(is_faulty=True)
    free_bikes = Bike.objects.all().filter(in_use=False)
    move_stations = Station.objects.all().filter(~Q(station_name=bike.station.station_name))

    context = {
        'faulty_bikes': faultybikes,
        'free_bikes': free_bikes,
        'move_stations': move_stations}

    return render(request, 'operator_page.html', context=context)

def manager_page(request):

    previous_orders = Order.objects.all().filter(is_complete=False)

    return render(request, 'manager_page.html', context={'previous_orders':previous_orders})

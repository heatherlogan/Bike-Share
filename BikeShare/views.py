from django.shortcuts import render, get_object_or_404, redirect
from .models import Bike, Station, Order
from account.models import Account
import datetime
from .forms import TopUpForm, PayBalanceForm, LocationForm
from django.core import serializers


def home(request):
    # all_stations = Station.objects.all()
    all_stations = serializers.serialize("json", Station.objects.all())
    context = {
        'all_stations': all_stations
    }
    return render(request, 'home.html', context=context)


def city_map(request):
    all_stations_map = serializers.serialize("json", Station.objects.all())
    return render(request, 'city_map.html.html', context={'all_stations_map':all_stations_map})


def customer_page(request):

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    customers_orders = Order.objects.all().filter()
    all_stations_map = serializers.serialize("json", Station.objects.all())

    form = LocationForm()
    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'customers_orders': customers_orders,
        'form': form,
        'all_stations_map': all_stations_map}

    return render(request, 'customer_page.html', context=context)


def rent_bike(request, station_id):

    # create new order with customer id, bike id, station id, start time.

    station = get_object_or_404(Station, pk=station_id)
    bike = station.bike_set.all().filter(in_use=False, is_faulty=False).first()
    rented_bike = get_object_or_404(Bike, pk=bike.id)
    user = get_object_or_404(Account, pk=request.POST.get('user_id', False))

    time = datetime.datetime.now()

    user.hires_in_progress += 1
    user.save()

    new_order = Order(bike=rented_bike, user=user, start_station=station, start_time=time)
    new_order.save()

    bike.in_use = True
    bike.save()

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    customers_orders = Order.objects.all()
    context = {
        'user':user,
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'customers_orders':customers_orders,
    }
    return render(request, 'customer_page.html', context=context)


def return_bike(request, order_id):

    def calculate_cost(starttime, endtime):
        if starttime.date() == endtime.date():
            hours_used = endtime.hour - starttime.hour
            cost = (hours_used + 1) * 5.00
        else:
            cost = 30.0 * (endtime.day - starttime.day)
        return cost

    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            start_time = order.start_time
            end = datetime.datetime.now()
            location = form.cleaned_data['locations']
            station = get_object_or_404(Station, pk=location.pk)

            order.end_station = station
            order.check_out_time = end
            order_cost = calculate_cost(start_time, end)
            order.is_complete = True
            order.due_amount = order_cost

            userid = order.user
            user = get_object_or_404(Account, pk=userid.pk)
            user.amount_owed += order_cost
            user.hires_in_progress -= 1
            user.save()

            bike = get_object_or_404(Bike, pk=order.bike.pk)
            bike.in_use = False
            bike.save()

            order.save()

            return redirect('bikeshare:bikeshare-customer')

        else:
            form = LocationForm()

        all_stations = Station.objects.all()
        all_bikes = Bike.objects.all()
        customers_orders = Order.objects.all()

        context = {
            'form': form,
            'order':order,
            'all_stations': all_stations,
            'all_bikes': all_bikes,
            'customers_orders':customers_orders,
        }
    return render(request, 'return_bike.html', context=context)


def top_up_balance(request):
    form = TopUpForm()
    return render(request, 'top_up.html', {'form': form})


def submit_top_up(request):

    success_message = ""

    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            user = request.user
            money = int(form.cleaned_data['money'])
            user.wallet_balance += money
            success_message = "You have topped up by £{}".format(money)
            user.save()
    else:
        form = TopUpForm()

    if success_message:
        context = {'success_message':success_message, 'form':form}
    else:
        context = {'form':form}
    return render(request, 'top_up.html', context=context)


def pay_balance(request):

    form = PayBalanceForm()

    return render(request, 'pay_balance.html', context={'form':form})


def submit_pay_balance(request):

    msg = ""

    if request.method=='POST':
        form = PayBalanceForm(request.POST)
        if form.is_valid():
            user = request.user
            payment_amount = int(form.cleaned_data['money'])
            if payment_amount <= user.wallet_balance and payment_amount <= user.amount_owed:
                user.wallet_balance -= payment_amount
                user.amount_owed -= payment_amount
                user.save()
                if user.amount_owed == 0:
                    msg = "You have paid off all your balance!"
                else:
                    msg = "You have paid £{}. You still owe £{}".format(payment_amount, user.amount_owed)
            elif payment_amount > user.wallet_balance:
                msg = "You don't have enough money in your wallet"
            elif payment_amount > user.amount_owed:
                msg = "You don't owe this much"

            if msg:
                context = {'msg':msg, 'form':form}
            else:
                context = {'form':form}
        else:
            form = TopUpForm()
            context={'form':form}

        return render(request, 'pay_balance.html', context=context)


def report_faulty(request, order_id):

    order = get_object_or_404(Order, pk=order_id)
    order.fix_amount += 20.0
    order.save()

    bike = order.bike
    bike.is_faulty = True
    bike.save()

    all_stations = Station.objects.all()
    all_bikes = Bike.objects.all()
    customers_orders = Order.objects.all()

    context = {
        'all_stations': all_stations,
        'all_bikes': all_bikes,
        'customers_orders':customers_orders,
    }
    return render(request, 'customer_page.html', context=context)


def operator_page(request):

    faultybikes = Bike.objects.all().filter(is_faulty=True)
    all_bikes = Bike.objects.all().filter()

    move_stations = Station.objects.all()

    context = {
        'faulty_bikes': faultybikes,
        'all_bikes': all_bikes,
        'move_stations': move_stations}

    return render(request, 'operator_page.html', context=context)


def repair_bike(request, bike_id):

    bike = get_object_or_404(Bike, pk=bike_id)
    bike.is_faulty = False
    bike.save()

    faultybikes = Bike.objects.all().filter(is_faulty=True)
    all_bikes = Bike.objects.all().filter()
    move_stations = Station.objects.all()

    context = {
        'faulty_bikes': faultybikes,
        'all_bikes': all_bikes,
        'move_stations': move_stations}
    return render(request, 'operator_page.html', context=context)


def move_bike(request, bike_id):

    bike = get_object_or_404(Bike, pk=bike_id)
    msg =""
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data["locations"]
            if location != bike.station:
                msg = "You have moved bike from {} to {} Bike Station.".format(bike.station, location)
            else:
                msg = "Bike is already at {} Bike Station".format(bike.station)
            station = get_object_or_404(Station, pk=location.pk)
            bike.station = station
            bike.save()
        else:
            form = LocationForm()

        if msg:
            context = {'msg':msg,
                'bike': bike,
                       'form': form}
        else:
            context={'bike': bike, 'form': form}

    return render(request, 'move_bike.html', context=context)



def manager_page(request):

    previous_orders = Order.objects.all().filter(is_complete=True)

    return render(request, 'manager_page.html', context={'previous_orders':previous_orders})

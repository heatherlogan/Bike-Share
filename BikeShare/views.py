from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')


def customer_page(request):
    return render(request, 'customer_page.html')


def operator_page(request):
    return render(request, 'operator_page.html')


def manager_page(request):
    return render(request, 'manager_page.html')

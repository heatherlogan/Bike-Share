from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'bikeshare'

urlpatterns = [

    path('', views.home, name='bikeshare-main'),

    path('customer/', views.customer_page, name='bikeshare-customer'),
    path('customer/<int:station_id>/rent', views.rent_bike, name='rent_bike'),
    path('customer/<int:order_id>/return', views.return_bike, name='return_bike'),
    path('customer/<int:order_id>/report_faulty', views.report_faulty, name='report_faulty'),

    path('manager/', views.manager_page, name='bikeshare-manager'),
    path('operator/', views.operator_page, name='bikeshare-operator'),

]
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.home, name='bikeshare-main'),
    path('customer/', views.customer_page, name='bikeshare-customer'),
    path('manager/', views.manager_page, name='bikeshare-manager'),
    path('operator/', views.operator_page, name='bikeshare-operator'),

]
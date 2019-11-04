from django.contrib import admin
from django.urls import path, include
from . import views
from account.views import registration_view, logout_view, login_view


app_name = 'bikeshare'

urlpatterns = [

    path('', views.home, name='bikeshare-main'),
    path('howitworks/', views.how_it_works, name='howitworks'),
    path('login/', login_view, name='login'),
    path('signup/', registration_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('top-up/', views.top_up_balance, name='top-up'),
    path('top-up/submit/', views.submit_top_up, name='top-up-submit'),
    path('pay-balance/', views.pay_balance, name='pay-balance'),
    path('pay-balance/submit/', views.submit_pay_balance, name='pay-balance-submit'),

    path('customer/', views.customer_page, name='bikeshare-customer'),
    path('customer/<int:station_id>/rent', views.rent_bike, name='rent_bike'),
    path('customer/<int:order_id>/return', views.return_bike, name='return_bike'),
    path('customer/<int:order_id>/report_faulty', views.report_faulty, name='report_faulty'),

    path('manager/', views.manager_page, name='bikeshare-manager'),
    path('operator/', views.operator_page, name='bikeshare-operator'),
    path('operator/<int:bike_id>/repair_bike', views.repair_bike, name='repair_bike'),
    path('operator/<int:bike_id>/move_bike', views.move_bike, name='move_bike')

]
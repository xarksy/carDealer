from django.contrib import admin
from django.urls import path, include
from .views import carList, create_car

urlpatterns = [
    path('',carList,name='carList'),
    path('create/',create_car,name='create_car'),
]

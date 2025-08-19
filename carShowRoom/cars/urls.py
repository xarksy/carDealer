from django.contrib import admin
from django.urls import path, include
from .views import carList, create_car, detail_car, updateCar

urlpatterns = [
    path('',carList,name='carList'),
    path('create/',create_car,name='create_car'),
    path('detail/<int:car_id>', detail_car, name='detail_car'),
    path('update/<int:car_id>', updateCar, name='update_car'),
]

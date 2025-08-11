from django.contrib import admin
from django.urls import path, include
from .views import carList

urlpatterns = [
    path('',carList,name='carList'),
]

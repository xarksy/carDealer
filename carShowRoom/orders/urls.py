from django.contrib import admin
from django.urls import path
from .views import placing_order_view

urlpatterns = [
    path('', placing_order_view, name='orders'),
]

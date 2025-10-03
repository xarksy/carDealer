from django.contrib import admin
from django.urls import path, include
from .views import login_view, logout_view
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('cars.urls')),    
    path('login/',login_view, name='login'),
    path('logout/',logout_view,name='logout'),
    path('users/',include('users.urls')),
    path('orders/',include('orders.urls')),
    path('api/',include('cars.api.urls')),
]

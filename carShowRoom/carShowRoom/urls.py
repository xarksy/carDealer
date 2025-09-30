from django.contrib import admin
from django.urls import path, include
from .views import login_view, logout_view
from rest_framework.routers import DefaultRouter
from cars.api import CarsViewSet

router = DefaultRouter()
router.register(r'cars', CarsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('cars.urls')),    
    path('login/',login_view, name='login'),
    path('logout/',logout_view,name='logout'),
    path('users/',include('users.urls')),
    path('orders/',include('orders.urls')),
    path('api/',include(router.urls)),
]

from django.urls import path
from .views import demo_api_dashboard, demo_login, demo_logout

urlpatterns = [
    path('login/', demo_login, name='demo_login'),
    path('dashboard/', demo_api_dashboard, name='demo_dashboard'),
    path('logout/', demo_logout, name='demo_logout'),
]

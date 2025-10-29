from django.urls import path
from .views import dashboard_of_dashboard, demo_login, demo_logout, demo_carlist_dashboard
from users.views import userlist_view

urlpatterns = [
    path('login/', demo_login, name='demo_login'),
    path('dashboard/', dashboard_of_dashboard, name='demo_dashboard'),
    path('dashboard/carlist/', demo_carlist_dashboard, name='demo_carlist_dashboard'),
    path('dashboard/userlist/', userlist_view, name='demo_userlist_dashboard'),
    path('logout/', demo_logout, name='demo_logout'),
]

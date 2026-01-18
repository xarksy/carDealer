from django.urls import path
from .views import dashboard_of_dashboard, demo_login, demo_logout, demo_carlist_dashboard, dashboard_customer_list, demo_api
from users.views import userlist_view
from activity_log.views import dashboard_log

urlpatterns = [
    path('login/', demo_login, name='demo_login'),
    path('dashboard/', dashboard_of_dashboard, name='demo_dashboard'),
    path('dashboard/userlist/', userlist_view, name='demo_userlist_dashboard'),
        path('dashboard/logs/', dashboard_log, name='dashboard_log_list'),
    path('dashboard/carlist/', demo_carlist_dashboard, name='demo_carlist_dashboard'),
    path('dashboard/customerlist/', dashboard_customer_list, name='demo_customer_list_dashboard'),
    path('api/', demo_api, name='demo_api'),
    path('logout/', demo_logout, name='demo_logout'),
]

from django.contrib import admin
from django.urls import path, include
from .views import carList, create_car, detail_car, updateCar, deleteCar, car_service_plain, car_service, dashboard_car_list, success_page, dashboard_customer_list, dashboard_of_dashboard
from users.views import userlist_view

urlpatterns = [
    path('',carList,name='carList'),
    path('create/',create_car,name='create_car'),
    path('detail/<int:car_id>/', detail_car, name='detail_car'),
    path('update/<int:car_id>/', updateCar, name='update_car'),
    path('delete/<int:car_id>/', deleteCar, name='delete_car'),
    path('service/',car_service_plain,name='car_service'),
    path('service/<int:car_id>/', car_service, name='service_history'),
    path('dashboard/',dashboard_of_dashboard, name='dashboard'),
    path('dashboard/user_list/', userlist_view, name='dashboard_user_list'),
    path('dashboard/car_list/',dashboard_car_list, name='dashboard_car_list'),
    path('dashboard/customer_list/',dashboard_customer_list, name='dashboard_customer_list'),
    path('success/',success_page, name='success_page'),
]

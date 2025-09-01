from django.urls import path
from .views import userView, register_view, userlist_view

urlpatterns = [
    path('', userView, name='user_view'),
    path('userlist/', userlist_view, name='user_list'),
    path('register/', register_view, name='register'),
]
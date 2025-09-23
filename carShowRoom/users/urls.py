from django.urls import path
from .views import userView, register_view, userlist_view, update_user_view, delete_user_view

urlpatterns = [
    path('', userlist_view, name='user_list'),
    # path('userlist/', userlist_view, name='user_list'),
    path('register/', register_view, name='register'),    
    path('update/<int:user_id>/', update_user_view, name='update_user'),
    path('delete/<int:user_id>/', delete_user_view, name='delete_user'),
]
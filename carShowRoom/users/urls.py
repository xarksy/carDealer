from django.urls import path
from .views import userView

urlpatterns = [
    path('', userView, name='user_view'),
]
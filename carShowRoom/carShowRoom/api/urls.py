from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView, UserProfileView

urlpatterns = [
    path('token/',CustomTokenObtainPairView.as_view(), name='token_obtain_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include('cars.api.urls')),
    path('', include('orders.api.urls')),
    path('', include('customer.api.urls')),
    path('', include('users.api.urls')),

]

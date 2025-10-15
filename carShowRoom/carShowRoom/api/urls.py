from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('', include('cars.api.urls')),
    path('', include('orders.api.urls')),
    # path('', include('customers.api.urls')),    
]

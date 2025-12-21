from django.contrib import admin
from django.urls import path, include
from .views import login_view, logout_view, api_login

# untuk display image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('cars.urls')),    
    path('login/',login_view, name='login'),
    path('logout/',logout_view,name='logout'),
    path('users/',include('users.urls')),
    path('orders/',include('orders.urls')),
    path('api/',include('carShowRoom.api.urls')),
    path('login_api/',api_login, name='login_api'),
    path('demo/',include('demo.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
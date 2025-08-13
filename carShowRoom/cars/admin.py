from django.contrib import admin
from .models import Cars, ServiceHistory

# Register your models here.
admin.site.register(Cars)
admin.site.register(ServiceHistory)
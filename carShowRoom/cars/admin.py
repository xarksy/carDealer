from django.contrib import admin
from .models import Cars, ServiceHistory, CarImage

# Register your models here.
admin.site.register(Cars)
admin.site.register(ServiceHistory)


# 1. Tampilan inline untuk gambar
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3 # Menampilkan 3 slot upload kosong secara default

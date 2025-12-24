from django.contrib import admin
from .models import Cars, ServiceHistory, CarImage

# 1. Tampilan inline untuk gambar
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3 # Menampilkan 3 slot upload kosong secara default

# 2. Masukkan Inline tersebut ke dalam Admin Mobil
class CarAdmin(admin.ModelAdmin):
    # Menambahkan fitur upload banyak gambar di halaman edit mobil
    inlines = [CarImageInline]

    list_display = ('nama','merek','harga','status')


# Register your models here.
admin.site.register(Cars)
admin.site.register(ServiceHistory)
admin.site.register(CarAdmin)



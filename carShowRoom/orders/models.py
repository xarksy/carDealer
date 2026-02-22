from django.db import models
from customer.models import Customer
from cars.models import Cars

# Create your models here.
class TradeInCar(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    offered_vehicle_model = models.CharField(max_length=100, blank=True, null=True)    
    offered_vehicle_varian = models.CharField(max_length=100, blank=True, null=True)
    offered_vehicle_transmission = models.CharField(max_length=20, choices=[('auto','Otomatis'), ('manual', 'Manual')], blank=True, null=True)
    offered_vehicle_province = models.CharField(max_length=50, blank=True, null=True)
    offered_vehicle_year = models.IntegerField(blank=True, null=True)
    offered_vehicle_kilometers = models.IntegerField(blank=True, null=True)
    offered_vehicle_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.model} - {self.customer.name}"

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ("sell","Sell"),
        ("trade","Trade"),
        ("buy","Buy"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    showroom_car = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True, blank=True)
    offer_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    trade_in_car = models.OneToOneField(TradeInCar, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.offer_type} - {self.customer.name}"



# --- UPDATE KODE INI DI BARIS PALING BAWAH orders/models.py ---
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Customer)
def update_car_status_on_customer_status_change(sender, instance, created, **kwargs):
    """
    Fungsi ini berjalan otomatis setiap data Customer di-update.
    - Jika 'deal' -> Mobil jadi 'booked'
    - Jika 'not_deal' atau 'rna' -> Mobil kembali 'available'
    """
    # Ambil semua order yang terkait dengan customer ini
    customer_orders = instance.orders.all()
    
    for order in customer_orders:
        car = order.showroom_car
        
        # Pastikan customer ini mengincar mobil showroom tertentu
        if car:
            # SKENARIO 1: Customer Deal
            if instance.status == 'deal':
                # Hanya ubah jika mobil masih available
                if car.status == 'available':
                    car.status = 'booked'
                    car.save()
            
            # SKENARIO 2: Customer Batal (Not Deal / RNA)
            elif instance.status in ['not_deal', 'rna']:
                # Hanya kembalikan ke available jika statusnya sedang 'booked'
                # (Penting: agar tidak merubah status mobil yang ternyata sudah 'sold')
                if car.status == 'booked':
                    car.status = 'available'
                    car.save()
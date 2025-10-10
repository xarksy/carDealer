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


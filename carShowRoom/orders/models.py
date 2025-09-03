from django.db import models
from customer.models import Customer
from cars.models import Car

# Create your models here.
class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ("sell","Sell"),
        ("trade","Trade"),
        ("buy","Buy"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    showroom_car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
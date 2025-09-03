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

    
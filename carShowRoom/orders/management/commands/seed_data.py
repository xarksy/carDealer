from django.core.management.base import BaseCommand
from faker import Faker
from cars.models import Cars
from customer.models import Customer
from orders.models import Order
import random

class Command(BaseCommand):
    help = "Seed the database with demo data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Seed Cars
        for _ in range(10):
            Cars.objects.get_or_create(
                nama=fake.word().capitalize(),
                mere=fake.company(),
                harga=random.randint(100000000,500000000)
            )
        
        
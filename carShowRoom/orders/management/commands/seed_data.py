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
        
        # Seed Customers
        for _ in range(5):
            Customer.objects.get_or_create(
                nama=fake.name(),
                email=fake.email(),
                phone=fake.phone_number()
            )
        
        # Seed Orders
        cars = list(Cars.objects.all())
        customers = list(Customer.objects.all())
        for _ in range(15):
            Order.objects.get_or_create(
                customer=random.choice(customers),
                car=random.choice(cars),
            )
        
        self.stdout.write(self.style.SUCCESS("🌱 Database seeded successfully!"))
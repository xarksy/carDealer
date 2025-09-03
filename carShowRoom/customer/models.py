from django.db import models

class Customer(models.Model):
    STATUS_CHOICES = [
        ("deal","Deal"),
        ("negotiating","Negotiating"),
        ("not_deal", "Not Deal"),
        ("uncontacted", "Uncontacted"),
        ("rna","RNA (Return, No Answer)"),
    ]

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="uncontacted")
    
    # tracking waktu
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.customer_type}, {self.status})"

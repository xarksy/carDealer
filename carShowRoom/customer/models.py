from django.db import models

class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ("seller", "Seller"),
        ("trade_in", "Trade-In"),
        ("buyer", "Buyer"),
    ]

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

    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="uncontacted")
    
    # tracking waktu
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.customer_type}, {self.status})"

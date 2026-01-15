from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class UserLog(models.Model):
    # Pilihan aksi agar seragam
    ACTION_CHOICES = [
        ('CREATE', 'Create Data'),
        ('UPDATE', 'Update Data'),
        ('DELETE', 'Delete Data'),
        ('LOGIN', 'Login System'),
        ('LOGOUT', 'Logout System'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target_model = models.CharField(max_length=50) # Misal: "Mobil", "Customer"
    description = models.TextField() # Detail : "Menambahkan mobil Honda Jazz"
    timestamp = models.DateTimeField(auto_now_add=True) # Otomatis isi waktu sekarang

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

from django.db import models

# Create your models here.
class Cars(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=12, decimal_places=2)
    merek = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    tahun = models.IntegerField()
    kilometer = models.IntegerField()
    transmisi = models.CharField(max_length=20, choices=[('auto','Otomatis'), ('manual', 'Manual')])
    jenis_bahan_bakar = models.CharField(max_length=20, choices=[('bensin','Bensin'), ('diesel', 'Diesel'), ('elektrik', 'Elektrik')])
    mesin = models.CharField(max_length=50)
    tempat_duduk = models.IntegerField()
    deskripsi = models.TextField()
    gambar = models.ImageField(upload_to='cars/images/',blank=True, null=True)

    def __str__(self):
        return self.nama

class ServiceHistory(models.Model):
    mobil = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='service_histories')
    tanggal_service = models.DateField()
    deskripsi = models.TextField()
    biaya = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Service on {self.tanggal_service} for {self.mobil.nama}"
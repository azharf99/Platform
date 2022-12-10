from django.db import models
from ekskul.models import Extracurricular

# Create your models here.

class Inventory(models.Model):
    pilihan_status = (
        ("Tersedia", "Tersedia"),
        ("Rusak", "Rusak"),
        ("Hilang", "Hilang"),
        ("Dipinjam", "Dipinjam"),
    )
    nama_barang = models.CharField(max_length=100)
    jumlah_total = models.PositiveIntegerField(default=0)
    jumlah_tersedia = models.PositiveIntegerField(default=0)
    jumlah_hilang = models.PositiveIntegerField(default=0)
    pemilik = models.ForeignKey(Extracurricular, on_delete=models.SET_NULL, null=True)
    tanggal_dibeli = models.DateField()
    anggaran_dana = models.FloatField(default=0.0)
    nama_toko = models.CharField(max_length=100, default="Tidak ada data")
    alamat_toko = models.TextField(max_length=250, default="Tidak ada data")
    status = models.CharField(max_length=100, choices=pilihan_status)

    def __str__(self):
        return self.nama_barang

class BuktiPembayaran(models.Model):
    barang = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    foto_nota = models.FileField(upload_to='nota-barang', default='blank-nota.png')

    def __str__(self):
        return self.foto_nota
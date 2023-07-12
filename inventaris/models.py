from django.db import models
from ekskul.models import Extracurricular


# Create your models here.

class Inventory(models.Model):
    pilihan_hibah = (
        (None, "Apakah ini barang hibah?"),
        ("Ya", "Ya"),
        ("Tidak", "Tidak"),
    )

    nama_barang = models.CharField(max_length=100)
    jumlah = models.PositiveIntegerField(default=0)
    pemilik = models.ForeignKey(Extracurricular, on_delete=models.SET_NULL, null=True)
    hibah = models.CharField(max_length=30, choices=pilihan_hibah)
    pemberi_hibah = models.CharField(max_length=100, blank=True)
    tanggal_hibah = models.DateField(blank=True, null=True)
    tanggal_dibeli = models.DateField(blank=True, null=True)
    anggaran_dana = models.FloatField(blank=True)
    nama_toko = models.CharField(max_length=100, blank=True)
    alamat_toko = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return '%s %s' % (self.nama_barang, self.pemilik)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"


class InventoryStatus(models.Model):
    pilihan_status = (
        ("Tersedia", "Tersedia"),
        ("Rusak", "Rusak"),
        ("Hilang", "Hilang"),
        ("Dipinjam", "Dipinjam"),
    )
    barang = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=pilihan_status, default="Tersedia")
    peminjam = models.CharField(max_length=200, blank=True)
    keterangan = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.barang, self.status)

    class Meta:
        verbose_name = "Inventory Status"
        verbose_name_plural = "Inventory Status"

class Invoice(models.Model):
    barang = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    foto_nota = models.FileField(upload_to='inventaris/nota', default='blank-nota.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.foto_nota

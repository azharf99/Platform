from django.db import models

# Create your models here.

class DeskripsiHome(models.Model):
    nama_bidang = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=250)
    url = models.CharField(max_length=100, default="not-available")
    color = models.CharField(max_length=50, default="primary")

    def __str__(self):
        return self.nama_bidang


class DeskripsiEkskul(models.Model):
    nama_aplikasi = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=200)
    url = models.CharField(max_length=100, default="ekskul:data-index")
    color = models.CharField(max_length=50, default="primary")

    def __str__(self):
        return self.nama_aplikasi
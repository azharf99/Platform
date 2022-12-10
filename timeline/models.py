from django.db import models


# Create your models here.

class Timeline(models.Model):
    tanggal = models.DateField()
    acara = models.CharField(max_length=200)
    tempat = models.CharField(max_length=200)
    penanggung_jawab = models.CharField(max_length=100)



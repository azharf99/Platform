from django.db import models
from ekskul.models import Teacher, Extracurricular


# Create your models here.

class Report(models.Model):
    nama_ekskul = models.CharField(max_length=100)
    nama_pembina = models.CharField(max_length=100)
    tanggal_pembinaan = models.DateField(auto_now=True)


class Image(models.Model):
    ekskul = models.ForeignKey(Report, on_delete=models.CASCADE)
    # foto = models.ImageField(upload_to=)
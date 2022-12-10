from django.db import models
from ekskul.models import Extracurricular, Teacher

# Create your models here.

class Report(models.Model):
    nama_ekskul = models.ForeignKey(Extracurricular)
    nama_pembina = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    tanggal_pembinaan = models.DateField()


class UploadImage(models.Model):
    ekskul = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True)
    foto = models.ImageField(upload_to='laporan-bulanan')
from django.db import models
from ekskul.models import Student, Extracurricular

# Create your models here.

class Penilaian(models.Model):
    nama_siswa = models.ForeignKey(Student, on_delete=models.CASCADE)
    nama_ekskul = models.ForeignKey(Extracurricular, on_delete=models.CASCADE)
    nilai = models.FloatField()

    def __str__(self):
        return f'%s %s' % (self.nama_ekskul, self.nama_siswa)

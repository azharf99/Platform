from django.db import models
from ekskul.models import Student, Extracurricular, StudentOrganization

# Create your models here.

class Penilaian(models.Model):
    # nama_ekskul = models.ForeignKey(Extracurricular, on_delete=models.SET_NULL, null=True)
    # nama_siswa = models.ForeignKey(Student, on_delete=models.CASCADE)
    siswa = models.ForeignKey(StudentOrganization, on_delete=models.CASCADE)
    nilai = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'%s %s' % (self.siswa, self.nilai)


    class Meta:
        verbose_name = "Penilaian"
        verbose_name_plural = "Penilaian"
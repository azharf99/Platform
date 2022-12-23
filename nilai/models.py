from django.db import models
from ekskul.models import StudentOrganization

# Create your models here.

class Penilaian(models.Model):
    pilih_nilai = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
    )
    siswa = models.ForeignKey(StudentOrganization, on_delete=models.CASCADE)
    nilai = models.CharField(max_length=3, choices=pilih_nilai)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'%s %s' % (self.siswa, self.nilai)


    class Meta:
        verbose_name = "Penilaian"
        verbose_name_plural = "Penilaian"
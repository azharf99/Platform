from django.db import models
from ekskul.models import Extracurricular, StudentOrganization, Teacher
from ekskul.compress_image import CompressedImageField


# Create your models here.

class Report(models.Model):
    nama_ekskul = models.ForeignKey(Extracurricular, on_delete=models.CASCADE)
    pembina_ekskul = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    tanggal_pembinaan = models.DateField()
    catatan_pembinaan = models.TextField(max_length=200, blank=True)
    kehadiran_santri = models.ManyToManyField(StudentOrganization)
    foto = CompressedImageField(upload_to='ekskul/laporan', default='no-image.png', quality=50, help_text="Format foto .jpg atau .jpeg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.tanggal_pembinaan.__format__("%d %B %Y"), self.nama_ekskul)


# class UploadImage(models.Model):
#     laporan = models.ForeignKey(Report, on_delete=models.CASCADE)
#     foto_absensi = CompressedImageField(upload_to='ekskul/laporan', default='no-image.png', quality=50, help_text="Format foto .jpg atau .jpeg")
#
#     def __str__(self):
#         return '%s' % (self.laporan)

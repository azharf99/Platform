from django.db import models
from ekskul.models import Teacher, Student
from ekskul.compress_image import CompressedImageField

# Create your models here.

class BidangOSN(models.Model):
    nama_bidang = models.CharField(max_length=50, verbose_name="Nama Bidang OSN")
    pembimbing = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    jadwal_bimbingan = models.TextField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return "%s" % (self.nama_bidang.capitalize())


class SiswaOSN(models.Model):
    bidang_osn = models.ForeignKey('BidangOSN', on_delete=models.CASCADE)
    nama_siswa = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return "%s | %s" % (self.bidang_osn.nama_bidang.upper(), self.nama_siswa)

class LaporanOSN(models.Model):
    pembimbing_osn = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    bidang_osn = models.ForeignKey(BidangOSN, on_delete=models.CASCADE)
    tanggal_pembinaan = models.DateField()
    kehadiran_santri = models.ManyToManyField(SiswaOSN)
    foto_bimbingan = CompressedImageField(upload_to='ekskul/osn', default='no-image.png', quality=50, help_text="Format foto harus .jpg atau .jpeg")
    materi_pembinaan = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.tanggal_pembinaan.__format__("%d %B %Y"), self.pembimbing_osn)

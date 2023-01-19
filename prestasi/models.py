from django.db import models

# Create your models here.
pilihan = (
    (1, "Ada"),
    (0, "Tidak Ada"),
)

class Prestasi(models.Model):
    kategori = models.CharField(max_length=100)
    jenis_lomba = models.CharField(max_length=100)
    tingkat_lomba = models.CharField(max_length=100)
    tahun_lomba = models.DateField()
    nama_lomba = models.CharField(max_length=100)
    Penyelenggara_lomba = models.CharField(max_length=100)
    peraih_prestasi = models.CharField(max_length=100)
    sekolah = models.CharField(max_length=100, default="SMAS IT Al Binaa")
    bidang_lomba = models.CharField(max_length=100)
    kategori_kemenangan = models.CharField(max_length=100)
    dokumentasi = models.BooleanField(choices=pilihan, default=0)
    sertifikat_1 = models.ImageField(upload_to='prestasi/sertifikat', null=True, blank=True)
    sertifikat_2 = models.ImageField(upload_to='prestasi/sertifikat', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s %s %s" % (self.kategori_kemenangan, self.nama_lomba, self.tahun_lomba, self.peraih_prestasi)

class DokumentasiPrestasi(models.Model):
    prestasi = models.ForeignKey('Prestasi', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='prestasi', blank=True, null=True, default='no-image.png')
    created_at = models.DateTimeField(default='2023-01-19')
    updated_at = models.DateTimeField(default='2023-01-19')

    def __str__(self):
        return self.prestasi

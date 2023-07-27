from django.db import models

# Create your models here.

class Prestasi(models.Model):
    kategori = models.CharField(max_length=100)
    jenis_lomba = models.CharField(max_length=100)
    tingkat_lomba = models.CharField(max_length=100)
    tahun_lomba = models.CharField(max_length=4)
    nama_lomba = models.CharField(max_length=100)
    Penyelenggara_lomba = models.CharField(max_length=100)
    peraih_prestasi = models.CharField(max_length=100)
    kelas_peraih_prestasi = models.CharField(max_length=100, null=True, blank=True)
    sekolah = models.CharField(max_length=100, default="SMAS IT Al Binaa")
    bidang_lomba = models.CharField(max_length=100)
    kategori_kemenangan = models.CharField(max_length=100)
    sertifikat_1 = models.FileField(upload_to='prestasi/sertifikat', null=True, blank=True)
    sertifikat_2 = models.FileField(upload_to='prestasi/sertifikat', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s %s %s" % (self.kategori_kemenangan, self.nama_lomba, self.tahun_lomba, self.peraih_prestasi)

class DokumentasiPrestasi(models.Model):
    prestasi = models.ForeignKey('Prestasi', on_delete=models.CASCADE)
    foto = models.FileField(upload_to='prestasi', blank=True, null=True, default='no-image.png')
    keterangan = models.TextField(max_length=300, blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.prestasi.nama_lomba, self.prestasi.peraih_prestasi)

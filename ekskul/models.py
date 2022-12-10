from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    no_hp = models.IntegerField(blank=True, default=0)
    foto = models.ImageField(upload_to='user', default='blank-profile.png')



class Teacher(models.Model):
    nama = models.OneToOneField('User', on_delete=models.CASCADE)
    nama_lengkap = models.CharField(max_length=100)
    niy = models.IntegerField(default=0)
    gelar_depan = models.CharField(max_length=20, blank=True)
    gelar_belakang = models.CharField(max_length=20, blank=True)
    jabatan = models.CharField(max_length=20, blank=True)
    jabatan_khusus = models.CharField(max_length=50, blank=True)


    def __str__(self):
        if self.gelar_depan or self.gelar_belakang:
            return f'%s %s, %s.' % (self.gelar_depan, self.nama_lengkap, self.gelar_belakang)
        else:
            return self.nama_lengkap


class Extracurricular(models.Model):
    hari = (
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
        ('Sabtu', 'Sabtu'),
        ('Ahad', 'Ahad'),
    )

    jenis = (
        ("Ekskul", "Ekstrakurikuler"),
        ("SC", "Study Club"),
    )

    pilihan_waktu = (
        ("Sore","Sore"),
        ("Malam","Malam"),
        ("Pagi","Pagi"),
        ("Siang","Siang"),
    )

    nama = models.CharField(max_length=50)
    pembina = models.ManyToManyField(Teacher)
    jadwal = models.CharField(max_length=15, choices=hari)
    waktu = models.CharField(max_length=15, choices=pilihan_waktu)
    jadwal_tambahan = models.CharField(max_length=20, choices=hari, default="Tidak ada", blank=True)
    waktu_tambahan = models.CharField(max_length=15, choices=pilihan_waktu, blank=True)
    tipe = models.CharField(max_length=20, choices=jenis, blank=True)

    def __str__(self):
        return self.nama


class Student(models.Model):
    pilih_kelas = (
        ('X-MIPA-A', 'X-MIPA-A'),
        ('X-MIPA-B', 'X-MIPA-B'),
        ('X-MIPA-C', 'X-MIPA-C'),
        ('X-MIPA-D', 'X-MIPA-D'),
        ('X-MIPA-E', 'X-MIPA-E'),
        ('X-MIPA-F', 'X-MIPA-F'),
        ('X-MIPA-G', 'X-MIPA-G'),
        ('X-MIPA-H', 'X-MIPA-H'),
        ('XI-MIPA-A', 'XI-MIPA-A'),
        ('XI-MIPA-B', 'XI-MIPA-B'),
        ('XI-MIPA-C', 'XI-MIPA-C'),
        ('XI-MIPA-D', 'XI-MIPA-D'),
        ('XI-MIPA-E', 'XI-MIPA-E'),
        ('XI-MIPA-F', 'XI-MIPA-F'),
        ('XI-MIPA-G', 'XI-MIPA-G'),
        ('XI-MIPA-H', 'XI-MIPA-H'),
        ('XII-MIPA-A', 'XII-MIPA-A'),
        ('XII-MIPA-B', 'XII-MIPA-B'),
        ('XII-MIPA-C', 'XII-MIPA-C'),
        ('XII-MIPA-D', 'XII-MIPA-D'),
        ('XII-MIPA-E', 'XII-MIPA-E'),
        ('XII-MIPA-F', 'XII-MIPA-F'),
        ('XII-MIPA-G', 'XII-MIPA-G'),
        ('XII-MIPA-H', 'XII-MIPA-H'),
    )
    nama = models.CharField(max_length=100)
    nis = models.IntegerField(unique=True)
    nisn = models.IntegerField(unique=True)
    kelas = models.CharField(max_length=15, choices=pilih_kelas)
    ekskul = models.ManyToManyField(Extracurricular)

    def __str__(self):
        return self.nama

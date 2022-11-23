from django.db import models


# Create your models here.

class Teacher(models.Model):
    nama = models.CharField(max_length=100)
    niy = models.IntegerField()
    gelar_depan = models.CharField(max_length=20, blank=True)
    gelar_belakang = models.CharField(max_length=20, blank=True)
    jabatan = models.CharField(max_length=20, blank=True)
    jabatan_khusus = models.CharField(max_length=50, blank=True)
    no_hp = models.IntegerField()
    email = models.EmailField()
    foto = models.ImageField(upload_to='pembina', default='blank-profile.png')


    def __str__(self):
        return self.nama


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

    nama = models.CharField(max_length=50)
    pembina = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    jadwal = models.CharField(max_length=15, choices=hari)
    waktu = models.TimeField()

    def __str__(self):
        return self.nama


class Student(models.Model):
    nama = models.CharField(max_length=100)
    nis = models.IntegerField(unique=True)
    nisn = models.IntegerField(unique=True)
    kelas = models.CharField(max_length=15)
    kelas = models.CharField(max_length=15)
    ekskul = models.ManyToManyField(Extracurricular)

    def __str__(self):
        return self.nama

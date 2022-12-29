from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass
#     # no_hp = models.IntegerField(blank=True, default=0)
#     foto = models.ImageField(upload_to='user', default='blank-profile.png')



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Username",)
    nama_lengkap = models.CharField(max_length=100, verbose_name="Nama Pembina")
    niy = models.IntegerField(default=0, verbose_name='NIY')
    gelar_depan = models.CharField(max_length=20, blank=True)
    gelar_belakang = models.CharField(max_length=20, blank=True)
    jabatan = models.CharField(max_length=100, blank=True)
    jabatan_khusus = models.CharField(max_length=100, blank=True)
    email = models.EmailField(default='user@gmail.com')
    no_hp = models.IntegerField(blank=True, default=0)
    foto = models.ImageField(upload_to='user', default='blank-profile.png', blank=True, null=True)

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

    nama = models.CharField(max_length=50, verbose_name="Nama Ekskul")
    pembina = models.ManyToManyField(Teacher)
    jadwal = models.CharField(max_length=15, choices=hari, verbose_name="Jadwal Pembinaan")
    waktu = models.CharField(max_length=15, choices=pilihan_waktu)
    jadwal_tambahan = models.CharField(max_length=20, choices=hari, default="Tidak ada", blank=True)
    waktu_tambahan = models.CharField(max_length=15, choices=pilihan_waktu, blank=True)
    tipe = models.CharField(max_length=20, choices=jenis, blank=True)
    slug = models.SlugField(blank=True)
    logo = models.ImageField(upload_to='ekskul/logo', default='no-image.png', blank=True, null=True)

    def __str__(self):
        return self.nama


class Student(models.Model):
    pilih_kelas = (
        ('X-MIPA-A', 'X-A'),
        ('X-MIPA-B', 'X-B'),
        ('X-MIPA-C', 'X-C'),
        ('X-MIPA-D', 'X-D'),
        ('X-MIPA-E', 'X-E'),
        ('X-MIPA-F', 'X-F'),
        ('X-MIPA-G', 'X-G'),
        ('X-MIPA-H', 'X-H'),
        ('XI-MIPA-A', 'XI-A'),
        ('XI-MIPA-B', 'XI-B'),
        ('XI-MIPA-C', 'XI-C'),
        ('XI-MIPA-D', 'XI-D'),
        ('XI-MIPA-E', 'XI-E'),
        ('XI-MIPA-F', 'XI-F'),
        ('XI-MIPA-G', 'XI-G'),
        ('XI-MIPA-H', 'XI-H'),
        ('XII-MIPA-A', 'XII-A'),
        ('XII-MIPA-B', 'XII-B'),
        ('XII-MIPA-C', 'XII-C'),
        ('XII-MIPA-D', 'XII-D'),
        ('XII-MIPA-E', 'XII-E'),
        ('XII-MIPA-F', 'XII-F'),
        ('XII-MIPA-G', 'XII-G'),
        ('XII-MIPA-H', 'XII-H'),
    )
    nama = models.CharField(max_length=100)
    nis = models.IntegerField(unique=True)
    nisn = models.CharField(max_length=20)
    kelas = models.CharField(max_length=15, choices=pilih_kelas)

    def __str__(self):
        return '%s | %s' % (self.kelas, self.nama[:18])


class StudentOrganization(models.Model):
    ekskul_siswa = models.ForeignKey(Extracurricular, on_delete=models.CASCADE)
    # pembina_ekskul = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    nama_siswa = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return "%s | %s" % (self.ekskul_siswa.slug.upper(), self.nama_siswa)

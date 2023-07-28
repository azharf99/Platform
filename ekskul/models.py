from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from ekskul.compress_image import CompressedImageField
from django.utils.text import slugify

jenis_kelamin = (
    ("L", "Laki-laki"),
    ("P", "Perempuan")
)

hari = (
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
        ('Sabtu', 'Sabtu'),
        ('Ahad', 'Ahad')
    )

jenis = (
        ("Ekskul", "Ekstrakurikuler"),
        ("SC", "Study Club")
    )

pilihan_waktu = (
        ("Sore","Sore"),
        ("Malam","Malam"),
        ("Pagi","Pagi"),
        ("Siang","Siang")
    )

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

# Create your models here.
class User(AbstractUser):
    pass
#     # no_hp = models.IntegerField(blank=True, default=0)
#     foto = models.ImageField(upload_to='user', default='blank-profile.png')



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Username",)
    niy = models.IntegerField(default=0, verbose_name='NIY')
    nama_pembina = models.CharField(max_length=100, verbose_name="Nama Pembina")
    jenis_kelamin = models.CharField(max_length=1, choices=jenis_kelamin, default="L")
    alamat = models.CharField(max_length=100, blank=True, null=True)
    jabatan = models.CharField(max_length=100, blank=True)
    email = models.EmailField(default='smaitalbinaa.ekskul@outlook.com', blank=True)
    no_hp = models.CharField(max_length=20, blank=True, default=0)
    foto = CompressedImageField(upload_to='user', default='blank-profile.png', blank=True, null=True, quality=50, help_text="format foto .jpg/.jpeg")

    def __str__(self):
        return self.nama_pembina

    class Meta:
        indexes = [
            models.Index(fields=["id","niy",]),
        ]


class Extracurricular(models.Model):
    nama_ekskul = models.CharField(max_length=50, verbose_name="Nama Ekskul")
    pembina = models.ManyToManyField(Teacher)
    jadwal = models.CharField(max_length=15, choices=hari, verbose_name="Jadwal Pembinaan")
    waktu = models.CharField(max_length=15, choices=pilihan_waktu)
    deskripsi = models.TextField(blank=True, null=True)
    tipe = models.CharField(max_length=20, choices=jenis, blank=True)
    slug = models.SlugField(blank=True)
    logo = CompressedImageField(upload_to='ekskul/logo', default='no-image.png', blank=True, null=True, quality=50, help_text="format logo .jpg/.jpeg")

    def __str__(self):
        return self.nama_ekskul

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nama_ekskul)
        super(Extracurricular, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ekskul:data-detail", kwargs={"slug": self.slug})

    class Meta:
        indexes = [
            models.Index(fields=["id", "slug",]),
        ]


class Student(models.Model):
    nis = models.CharField(max_length=20, unique=True)
    nisn = models.CharField(max_length=20, blank=True, null=True)
    nama_siswa = models.CharField(max_length=100)
    kelas = models.CharField(max_length=15, choices=pilih_kelas)
    jenis_kelamin = models.CharField(max_length=10, choices=jenis_kelamin, default="L")
    alamat = models.CharField(max_length=100, blank=True, null=True)
    tempat_lahir = models.CharField(max_length=50, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    nomor_hp = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, default="Aktif")
    foto = CompressedImageField(upload_to='student', blank=True, null=True, default='blank-profile.png', quality=50, help_text="Format foto .jpg/.jpeg")

    def __str__(self):
        return '%s | %s' % (self.kelas, self.nama_siswa)

    class Meta:
        indexes = [
            models.Index(fields=["nis", "id",]),
        ]


class StudentOrganization(models.Model):
    ekskul = models.ForeignKey(Extracurricular, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return "%s | %s" % (self.ekskul, self.siswa)

    def get_absolute_url(self):
        return reverse("ekskul:input-anggota", kwargs={"slug":self.ekskul.slug})



from django.db import models
from ekskul.models import Extracurricular, Teacher, Student
# Create your models here.

def proposal_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/proposal/<username>/<filename>
    return 'proposal/{0}/{1}'.format(instance.user.username, filename)

class Proposal(models.Model):
    pilihan_tingkat = (
        (None, "Pilih Tingkat Event"),
        ("Desa", "Desa/Kelurahan"),
        ("Kecamatan", "Kecamatan"),
        ("Kabupaten", "Kabupaten"),
        ("Provinsi", "Provinsi"),
        ("Nasional", "Nasional"),
        ("Internasional", "Internasional"),
    )
    pilihan_pelaksaan = (
        (None,"Pilih Jenis Pelaksanaan"),
        ("Offline", "Offline"),
        ("Online", "Online"),
    )
    pilihan_berjenjang = (
        (None, "Apakah Lomba Berjenjang?"),
        ("Ya", "Ya"),
        ("Tidak", "Tidak"),
    )

    pilihan_target_sassaran = (
        (None, "Proposal event ini untuk siapa?"),
        ("Santri", "Santri"),
        ("Ustadz", "Ustadz"),
    )

    pilihan_jenis_proposal = (
        (None, "Mau mengajukan proposal gimana?"),
        ("Aplikasi", "Buat dan ajukan proposal melalui Aplikasi"),
        ("Upload", "Upload File Proposal yang sudah ada saja"),
    )

    nama_event = models.CharField(max_length=200)
    pembuat_event = models.CharField(max_length=200)
    tanggal_awal_pelaksanaan = models.DateField()
    tanggal_akhir_pelaksanaan = models.DateField()
    tingkat_event = models.CharField(max_length=30, choices=pilihan_tingkat)
    pelaksanaan = models.CharField(max_length=30, choices=pilihan_pelaksaan)
    berjenjang = models.CharField(max_length=50, choices=pilihan_berjenjang)
    terget_sasaran = models.CharField(max_length=20, choices=pilihan_target_sassaran)
    jenis_proposal = models.CharField(max_length=150, choices=pilihan_jenis_proposal)

    def __str__(self):
        return self.nama_event

class Detail_Proposal(models.Model):
    event = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    nama_item = models.CharField(max_length=250)
    volume = models.FloatField(default=1.0)
    satuan = models.CharField(max_length=50, blank=True)
    harga_per_item = models.FloatField()
    jumlah_harga = models.FloatField(default=(volume * harga_per_item), editable=False)

    def __str__(self):
        return '%s %s %s' % (self.event, self.nama_item, self.jumlah)


class Acara_Santri(Proposal):
    event = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    ustadz_penanggungjawab = models.ForeignKey(Teacher.nama.teacher.nama_lengkap, on_delete=models.CASCADE)
    ekskul = models.ForeignKey(Extracurricular, on_delete=models.SET_NULL, null=True,
                               verbose_name="ekskul_yang_terlibat")
    santri = models.ManyToManyField(Student.objects.filter(ekskul=ekskul), verbose_name="santri yang terlibat")
    anggaran_biaya = models.FloatField()
    upload_file = models.FileField(upload_to=proposal_directory_path, verbose_name="File Proposal")

class Acara_Ustadz(Proposal):
    event = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    ustadz = models.ForeignKey(Teacher.nama.teacher.nama_lengkap, on_delete=models.CASCADE)
    anggaran_biaya = models.FloatField()
    upload_file = models.FileField(upload_to=proposal_directory_path, verbose_name="File Proposal")
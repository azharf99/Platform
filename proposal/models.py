from django.db import models
from ekskul.models import Extracurricular, Teacher, Student
# Create your models here.

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
def proposal_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/proposal/<username>/<filename>
    return 'proposal/{0}/{1}'.format(instance.user.username, filename)

class ProposalSantri(models.Model):
    nama_event = models.CharField(max_length=200)
    pembuat_event = models.CharField(max_length=200)
    tanggal_awal = models.DateField(verbose_name="tanggal_awal_pelaksanaan")
    tanggal_akhir = models.DateField(verbose_name="tanggal_akhir_pelaksanaan")
    tingkat_event = models.CharField(max_length=30, choices=pilihan_tingkat)
    pelaksanaan = models.CharField(max_length=30, choices=pilihan_pelaksaan)
    berjenjang = models.CharField(max_length=50, choices=pilihan_berjenjang)
    penanggungjawab = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    ekskul = models.ForeignKey(Extracurricular, on_delete=models.SET_NULL, null=True,
                               verbose_name="ekskul_yang_terlibat")
    santri = models.ManyToManyField(Student, verbose_name="santri yang terlibat")
    anggaran_biaya = models.FloatField()
    upload_file = models.FileField(upload_to=proposal_directory_path, verbose_name="Upload File Proposal")

    def __str__(self):
        return self.nama_event

    class Meta:
        verbose_name = "Student Proposal"

class ProposalUstadz(models.Model):
    nama_event = models.CharField(max_length=200)
    pembuat_event = models.CharField(max_length=200)
    tanggal_awal_pelaksanaan = models.DateField()
    tanggal_akhir_pelaksanaan = models.DateField()
    tingkat_event = models.CharField(max_length=30, choices=pilihan_tingkat)
    pelaksanaan = models.CharField(max_length=30, choices=pilihan_pelaksaan)
    berjenjang = models.CharField(max_length=50, choices=pilihan_berjenjang)
    ustadz = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    anggaran_biaya = models.FloatField()
    upload_file = models.FileField(upload_to=proposal_directory_path, verbose_name="Upload File Proposal")

    def __str__(self):
        return self.nama_event

    class Meta:
        verbose_name = "Teacher Proposal"

# class Detail_Proposal(models.Model):
#     event = models.ForeignKey(Proposal_Santri, Proposal_Ustadz, on_delete=models.CASCADE)
#     nama_item = models.CharField(max_length=250)
#     volume = models.FloatField(default=1.0)
#     satuan = models.CharField(max_length=50, blank=True)
#     harga_per_item = models.FloatField()
#     jumlah_harga = models.FloatField(default=(volume * harga_per_item), editable=False)
#
#     def __str__(self):
#         return '%s %s %s' % (self.event, self.nama_item, self.jumlah)
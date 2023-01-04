from django.db import models
from ekskul.models import Extracurricular, Teacher, StudentOrganization

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
    (None, "Pilih Jenis Pelaksanaan"),
    ("Offline", "Offline"),
    ("Online", "Online"),
)
pilihan_berjenjang = (
    (None, "Apakah Lomba Berjenjang?"),
    ("Ya", "Ya"),
    ("Tidak", "Tidak"),
)

status_proposal = (
        ("Accepted", "Menerima"),
        ("Rejected", "Menolak"),
        ("Pending", "Menunda"),
        ("Some Info Required", "Membutuhkan informasi lebih detail"),
    )

status_proposal_bendahara = (
        ("Accepted", "Menerima"),
        ("Pending", "Menunda"),
        ("Some Info Required", "Membutuhkan informasi lebih detail"),
    )

class Proposal(models.Model):
    nama_event = models.CharField(max_length=200)
    pembuat_event = models.CharField(max_length=200)
    tanggal_pendaftaran = models.DateField()
    batas_pendaftaran = models.DateField(default="2022-12-29", blank=True, null=True)
    tanggal_penyisihan_1 = models.DateField(blank=True, null=True)
    tanggal_penyisihan_2 = models.DateField(blank=True, null=True)
    tanggal_penyisihan_3 = models.DateField(blank=True, null=True)
    tanggal_semifinal = models.DateField(blank=True, null=True)
    tanggal_final = models.DateField(blank=True, null=True)
    pengumuman_pemenang = models.DateField(blank=True, null=True)
    pelaksanaan = models.CharField(max_length=30, choices=pilihan_pelaksaan)
    tingkat_event = models.CharField(max_length=30, choices=pilihan_tingkat)
    berjenjang = models.CharField(max_length=50, choices=pilihan_berjenjang)
    lokasi_event = models.CharField(max_length=200, default="")
    kota = models.CharField(max_length=200, default="", verbose_name="Kota/Kabupaten")
    provinsi = models.CharField(max_length=200, default="")
    penanggungjawab = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    ekskul = models.ForeignKey(Extracurricular, on_delete=models.CASCADE, null=True, blank=True)
    santri = models.ManyToManyField(StudentOrganization, verbose_name="Santri yang ikut", blank=True, help_text="Pada PC/Laptop, tekan Ctrl untuk memilih banyak opsi")
    anggaran_biaya = models.FloatField()
    upload_brosur = models.FileField(upload_to='proposal/brosur', verbose_name="Upload Brosur Lomba", null=True, blank=True)
    upload_undangan = models.FileField(upload_to='proposal/undangan', verbose_name="Upload Undangan Lomba", null=True,
                                     blank=True)
    upload_file = models.FileField(upload_to='proposal', verbose_name="Upload File Proposal", help_text="Format file dalam bentuk .pdf")
    Catatan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_event


class ProposalStatus(models.Model):
    proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE)
    is_wakasek = models.CharField(max_length=100, choices=status_proposal, default="Pending", verbose_name="Keputusan Wakasek Ekskul")
    alasan_wakasek = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=20, default='Wakasek')
    foto_alasan = models.ImageField(upload_to='proposal/koreksi', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.is_wakasek


class ProposalStatusKepsek(models.Model):
    proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE)
    status_wakasek = models.ForeignKey('ProposalStatus', on_delete=models.CASCADE)
    is_kepsek = models.CharField(max_length=100, choices=status_proposal, default="Pending", verbose_name="Keputusan Kepala Sekolah")
    alasan_kepsek = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=20, default='Kepsek')
    foto_alasan = models.ImageField(upload_to='proposal/koreksi', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.is_kepsek

class ProposalStatusBendahara(models.Model):
    proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE)
    status_kepsek = models.ForeignKey('ProposalStatusKepsek', on_delete=models.CASCADE)
    is_bendahara = models.CharField(max_length=100, choices=status_proposal_bendahara, default="Pending", verbose_name="Keputusan Bendahara")
    alasan_bendahara = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=20, default='Bendahara')
    foto_alasan = models.ImageField(upload_to='proposal/koreksi', blank=True, null=True)
    bukti_transfer = models.ImageField(upload_to='proposal/transfer', blank=True, null=True)
    catatan_bendahara = models.TextField(max_length=200, default="Aman")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.is_bendahara

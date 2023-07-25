from django.db import models
from ekskul.models import Extracurricular, Teacher, Student
from ekskul.compress_image import CompressedImageField

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
    ("Hybrid", "Hybrid"),
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
    tanggal_pelaksanaan = models.DateField(blank=True, null=True)
    pelaksanaan = models.CharField(max_length=30, choices=pilihan_pelaksaan, verbose_name="Tempat Pelaksanaan")
    tingkat_event = models.CharField(max_length=30, choices=pilihan_tingkat)
    lokasi_event = models.CharField(max_length=200, default="")
    penanggungjawab = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    nomor_rekening = models.CharField(max_length=100, default="", verbose_name="Nomor Rekening PJ")
    nama_bank = models.CharField(max_length=100, default="Muamalat")
    ekskul = models.ForeignKey(Extracurricular, on_delete=models.CASCADE, null=True, blank=True)
    santri = models.ManyToManyField(Student, verbose_name="Santri yang terlibat", blank=True, help_text="Pada PC/Laptop, tekan Ctrl untuk memilih banyak opsi")
    anggaran_biaya = models.FloatField()
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
    foto_alasan = CompressedImageField(upload_to='proposal/transfer', blank=True, null=True, quality=50, help_text="Format file harus .jpeg atau .jpg")
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
    foto_alasan = CompressedImageField(upload_to='proposal/transfer', blank=True, null=True, quality=50, help_text="Format file harus .jpeg atau .jpg")
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
    bukti_transfer = CompressedImageField(upload_to='proposal/transfer', blank=True, null=True, quality=50, help_text="Format file harus .jpeg atau .jpg")
    catatan_bendahara = models.TextField(max_length=200, default="Aman")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.is_bendahara


class ProposalInventaris(models.Model):
    judul_proposal = models.CharField(max_length=200, verbose_name="Judul Proposal Pengadaan")
    tanggal_pembelian = models.DateField(verbose_name="Rencana tanggal pembelian", blank=True, null=True)
    nama_toko = models.CharField(max_length=200, blank=True, null=True)
    alamat_toko = models.CharField(max_length=200, blank=True, null=True)
    penanggungjawab = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    nomor_rekening = models.CharField(max_length=100, default="")
    nama_bank = models.CharField(max_length=100, default="Muamalat")
    ekskul = models.ForeignKey(Extracurricular, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Keperluan untuk ekskul")
    santri = models.ManyToManyField(Student, verbose_name="Keperluan untuk santri atas nama", blank=True, help_text="Pada PC/Laptop, tekan Ctrl untuk memilih banyak opsi")
    anggaran_biaya = models.FloatField()
    upload_file = models.FileField(upload_to='proposal', verbose_name="Upload File Proposal", help_text="Format file dalam bentuk .pdf")
    Catatan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judul_proposal


class ProposalInventarisStatus(models.Model):
    proposal = models.ForeignKey('ProposalInventaris', on_delete=models.CASCADE)
    is_wakasek = models.CharField(max_length=100, choices=status_proposal, default="Pending", verbose_name="Keputusan Wakasek Ekskul")
    alasan_wakasek = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=20, default='Wakasek')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.is_wakasek


class ProposalInventarisStatusKepsek(models.Model):
    proposal = models.ForeignKey('ProposalInventaris', on_delete=models.CASCADE)
    status_wakasek = models.ForeignKey('ProposalInventarisStatus', on_delete=models.CASCADE)
    is_kepsek = models.CharField(max_length=100, choices=status_proposal, default="Pending", verbose_name="Keputusan Kepala Sekolah")
    alasan_kepsek = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=20, default='Kepsek')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.is_kepsek

class ProposalInventarisStatusBendahara(models.Model):
    proposal = models.ForeignKey('ProposalInventaris', on_delete=models.CASCADE)
    status_kepsek = models.ForeignKey('ProposalInventarisStatusKepsek', on_delete=models.CASCADE)
    is_bendahara = models.CharField(max_length=100, choices=status_proposal_bendahara, default="Pending", verbose_name="Keputusan Bendahara")
    alasan_bendahara = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=20, default='Bendahara')
    bukti_transfer = models.ImageField(upload_to='proposal/transfer', blank=True, null=True)
    catatan_bendahara = models.TextField(max_length=200, default="Aman")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.is_bendahara
from django.shortcuts import render
from django.db.models import Count
from ekskul.models import Extracurricular, Student, StudentOrganization
from laporan.models import Report
from proposal.models import Proposal
from nilai.models import Penilaian
from userlog.models import UserLog
from osn.models import LaporanOSN, BidangOSN
from prestasi.models import Prestasi

# Create your views here.


def dashboard(request):
    data_ekskul = Extracurricular.objects.filter(tipe="Ekskul")
    data_sc = Extracurricular.objects.filter(tipe="SC")
    jumlah_siswa = Student.objects.all().count()
    siswa_ekskul = StudentOrganization.objects.values('siswa').annotate(dcount=Count('siswa')).count()
    ekskul_aktif = Report.objects.values('nama_ekskul__nama_ekskul').annotate(dcount=Count('nama_ekskul'))
    nama_ekskul = [x['nama_ekskul__nama_ekskul'] for x in ekskul_aktif]
    pertemuan_ekskul = [x['dcount'] for x in ekskul_aktif]
    laporan_ekskul = Report.objects.values('tanggal_pembinaan').annotate(dcount=Count('tanggal_pembinaan')).order_by('tanggal_pembinaan')
    laporan = Report.objects.all().order_by('-tanggal_pembinaan')[:5]
    data_pertemuan = [x['dcount'] for x in laporan_ekskul]
    data_tanggal = list(str(x['tanggal_pembinaan'].isoformat()) for x in laporan_ekskul)
    proposal = Proposal.objects.all()
    nilai = Penilaian.objects.all()
    logs = UserLog.objects.all().order_by('-created_at')[:5]
    osn = LaporanOSN.objects.values('bidang_osn__nama_bidang').annotate(dcount=Count('bidang_osn')).order_by()
    bidang_osn = list(x['bidang_osn__nama_bidang'] for x in osn)
    pertemuan_osn = list(x['dcount'] for x in osn)
    prestasi = Prestasi.objects.all().order_by('-created_at', '-tahun_lomba', 'peraih_prestasi')[:5]
    bidang_osn_qs = BidangOSN.objects.all().order_by('nama_bidang')

    context = {
        'data_ekskul': data_ekskul,
        'data_sc': data_sc,
        'data_ekskul_sc': data_ekskul.count() + data_sc.count(),
        'jumlah_siswa': jumlah_siswa,
        'siswa_ekskul': siswa_ekskul,
        'ekskul_aktif': ekskul_aktif.count(),
        'ekskul_nonaktif': (data_ekskul.count() + data_sc.count()) - ekskul_aktif.count(),
        'data_pertemuan': data_pertemuan,
        'data_tanggal': data_tanggal,
        'proposal': proposal,
        'nilai': nilai,
        'laporan': laporan,
        'logs': logs,
        'bidang_osn': bidang_osn,
        'pertemuan_osn': pertemuan_osn,
        'prestasi': prestasi,
        'nama_ekskul': nama_ekskul,
        'pertemuan_ekskul': pertemuan_ekskul,
        'bidang_osn_qs': bidang_osn_qs,
    }
    return render(request, 'new_index.html', context)
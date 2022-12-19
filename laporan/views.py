import datetime

from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from laporan.models import Report, UploadImage
from django.contrib.auth.decorators import login_required
from laporan.forms import LaporanKehadiran, UploadLaporanKehadiran
from ekskul.models import Extracurricular, StudentOrganization

# Create your views here.

def index(request):
    ekskul = Extracurricular.objects.all().order_by('tipe', 'nama')
    return render(request, 'laporan.html', context={'ekskul':ekskul})

def laporan_detail(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    bulan_ini = datetime.date.today().__format__("%B")
    filtered_report = Report.objects.filter(nama_ekskul__slug=slug).filter(tanggal_pembinaan__month=datetime.date.today().month).order_by('tanggal_pembinaan')
    context = {
        'ekskul': ekskul,
        'filtered_report': filtered_report,
        'bulan_ini': bulan_ini,
    }
    return render(request, 'laporan-detail.html', context)
@login_required(login_url='/admin/login')
def laporan_input(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    filtered_student = StudentOrganization.objects.filter(ekskul_siswa__slug=slug)
    for guru in ekskul.pembina.all():
        if not guru.nama.id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        nama_ekskul = request.POST.get('nama_ekskul')
        tanggal_pembinaan = request.POST.get('tanggal_pembinaan')
        kehadiran_santri = request.POST.get('kehadiran_santri')
        form = LaporanKehadiran(request.POST)
        LaporanKehadiran.nama_ekskul = nama_ekskul
        LaporanKehadiran.tanggal_pembinaan = tanggal_pembinaan
        LaporanKehadiran.kehadiran_santri = kehadiran_santri
        if form.is_valid():
            f = form.save()
            return redirect('laporan:laporan-upload', ekskul.slug)

    else:
        form = LaporanKehadiran()

    context = {
        'ekskul': ekskul,
        'filtered_student': filtered_student,
        'form': form,
    }
    return render(request, 'laporan-input.html', context)

@login_required(login_url='/admin/login')
def laporan_upload(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    filtered_report = Report.objects.filter(nama_ekskul__slug=slug)
    for guru in ekskul.pembina.all():
        if not guru.nama.id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        forms = UploadLaporanKehadiran(request.POST)
        id_laporan = request.POST.get('laporan')
        laporan = get_object_or_404(Report, id=id_laporan)
        images = request.FILES.getlist('images')

        for i in images:
            photo = UploadImage.objects.create(
                laporan=laporan,
                foto_absensi=i
            )

        return redirect('laporan:laporan-detail', ekskul.slug)
    else:
        forms = UploadLaporanKehadiran()

    context = {
        'ekskul': ekskul,
        'filtered_report': filtered_report,
        'forms': forms,
    }
    return render(request, 'laporan-upload.html', context)
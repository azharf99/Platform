import datetime
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from laporan.models import Report, UploadImage
from laporan.forms import LaporanKehadiran, UploadLaporanKehadiran
from ekskul.models import Extracurricular, StudentOrganization


# Create your views here.

def index(request):
    if request.GET.get('q') is not None or request.GET.get('q') == '':
        q = request.GET.get('q')
        ekskul = Extracurricular.objects.filter(
            Q(nama__icontains=q) | Q(pembina__nama_lengkap__icontains=q)).order_by('tipe', 'nama')
    else:
        ekskul = Extracurricular.objects.all().order_by('tipe', 'nama')
    context = {
        'ekskul': ekskul,
    }
    return render(request, 'laporan.html', context)


def laporan_detail(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    bulan_ini = datetime.date.today().__format__("%B")
    filtered_report = Report.objects.filter(nama_ekskul__slug=slug).filter(
        tanggal_pembinaan__month=datetime.date.today().month).order_by('tanggal_pembinaan')
    context = {
        'ekskul': ekskul,
        'filtered_report': filtered_report,
        'bulan_ini': bulan_ini,
    }
    return render(request, 'laporan-detail.html', context)


@login_required(login_url='/login/')
def laporan_input(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    filtered_student = StudentOrganization.objects.filter(ekskul_siswa__slug=slug)
    for guru in ekskul.pembina.all():
        if not guru.user_id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))

    nama_ekskul = request.POST.get('nama_ekskul')
    tanggal_pembinaan = request.POST.get('tanggal_pembinaan')
    kehadiran_santri = request.POST.get('kehadiran_santri')
    pembina = request.POST.get('pembina_ekskul')

    if request.method == 'POST':
        try:
            laporan = Report.objects.get(tanggal_pembinaan=tanggal_pembinaan)
            form = LaporanKehadiran(request.POST)
            messages.error(request, "Laporan untuk tanggal ini sudah ada. Silahkan pilih tanggal lain")
        except:
            form = LaporanKehadiran(request.POST)
            LaporanKehadiran.nama_ekskul = nama_ekskul
            LaporanKehadiran.tanggal_pembinaan = tanggal_pembinaan
            LaporanKehadiran.kehadiran_santri = kehadiran_santri
            LaporanKehadiran.pembina_ekskul = pembina
            if form.is_valid():
                form.save()
                return redirect('laporan:laporan-upload', ekskul.slug)

    else:
        form = LaporanKehadiran()

    context = {
        'ekskul': ekskul,
        'filtered_student': filtered_student,
        'form': form,
    }
    return render(request, 'laporan-input.html', context)


@login_required(login_url='/login/')
def laporan_upload(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    filtered_report = Report.objects.filter(nama_ekskul__slug=slug)
    for guru in ekskul.pembina.all():
        if not guru.user_id == request.user.id and not request.user.is_superuser:
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

@login_required(login_url='/login/')
def laporan_edit(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    laporan = get_object_or_404(Report, nama_ekskul__slug=slug, id=pk)
    for guru in ekskul.pembina.all():
        if not guru.user_id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        form = LaporanKehadiran(request.POST, instance=laporan)
        if form.is_valid():
            form.save()
            return redirect('laporan:laporan-detail', ekskul.slug)
        else:
            messages.error(request, "Mohon input data dengan benar!")
    else:
        form = LaporanKehadiran(instance=laporan)
    context = {
        'ekskul': ekskul,
        'form': form,
    }
    return render(request, 'laporan-edit.html', context)

@login_required(login_url='/login/')
def laporan_delete(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    laporan = get_object_or_404(Report, nama_ekskul__slug=slug, id=pk)
    for guru in ekskul.pembina.all():
        if not guru.user_id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        laporan.delete()
        return redirect('laporan:laporan-detail', ekskul.slug)
    context = {
        'ekskul': ekskul,
        'laporan': laporan,
    }

    return render(request, 'laporan-delete.html', context)


def laporan_upload_edit(request):
    return render(request)


def laporan_upload_delete(request):
    return render(request)

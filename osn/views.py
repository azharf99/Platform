import locale
import datetime
import pytz

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from osn.models import BidangOSN, SiswaOSN, LaporanOSN
from osn.forms import FormInputBidang, FormInputSiswa, FormInputLaporanOSN, FormEditLaporanOSN


# Create your views here.
class OsnIndexView(ListView):
    model = BidangOSN
    context_object_name = 'data'
    template_name = 'new_osn.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.teacher.bidangosn_set.count() > 0:
                return BidangOSN.objects.filter(pembimbing=self.request.user.teacher).order_by('nama_bidang')
            else:
                return BidangOSN.objects.all().order_by('nama_bidang')

        else:
            return BidangOSN.objects.all().order_by('nama_bidang')


@login_required(login_url='/login/')
def bidang_osn_input(request):
    if not request.user.is_superuser:
        return redirect('restricted')
    if request.method == "POST":
        forms = FormInputBidang(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('osn:osn-index')
        else:
            forms = FormInputBidang(request.POST)
            messages.error(request, "Yang kamu isi ada yang salah. Mohon cek ulang.")
    else:
        forms = FormInputBidang()
    context = {
        'forms': forms,
        'tipe': True,
        'name': 'Input Bidang OSN',
    }
    return render(request, 'new_osn-input.html', context)



@login_required(login_url='/login/')
def bidang_osn_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('restricted')

    data = get_object_or_404(BidangOSN, id=pk)

    if request.method == "POST":
        forms = FormInputBidang(request.POST, instance=data)
        if forms.is_valid():
            forms.save()
            return redirect('osn:osn-index')
        else:
            forms = FormInputBidang(instance=data)
            messages.error(request, "Yang kamu isi ada yang salah. Mohon cek ulang.")
    else:
        forms = FormInputBidang(instance=data)
    context = {
        'forms': forms,
        'name': 'Edit Bidang OSN',
    }
    return render(request, 'new_osn-input.html', context)


@login_required(login_url='/login/')
def bidang_osn_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('restricted')

    data = get_object_or_404(BidangOSN, id=pk)

    if request.method == "POST":
        data.delete()

    context = {
        'data': data,
    }
    return render(request, 'new_osn-delete.html', context)

class DetailBidangOSNView(DetailView):
    model = BidangOSN
    template_name = 'new_osn-detail.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_siswa'] = SiswaOSN.objects.filter(bidang_osn__slug=self.kwargs.get('slug')).order_by('nama_siswa__kelas', 'nama_siswa__nama_siswa')
        context['data_laporan'] = LaporanOSN.objects.filter(bidang_osn__slug=self.kwargs.get('slug')).order_by('tanggal_pembinaan')
        return context


@login_required(login_url='/login')
def siswa_osn_input(request, slug):
    if request.method == "POST":
        nama_siswa_id = request.POST.get('nama_siswa')
        forms = FormInputSiswa(request.POST)
        if SiswaOSN.objects.filter(nama_siswa_id=nama_siswa_id, bidang_osn__slug=slug).exists():
            forms = FormInputSiswa(request.POST)
            messages.error(request, "Siswa sudah ada di data. Slahkan pilih yang lain")
        elif forms.is_valid():
            forms.save()
            return redirect('osn:detail-bidang-osn', slug)
        else:
            forms = FormInputSiswa(request.POST)
            messages.error(request, "Yang kamu isi ada yang salah. Mohon cek ulang.")
    else:
        forms = FormInputSiswa()
    context = {
        'forms': forms,
        'slug': slug,
        'name': "Input Siswa OSN",
    }
    return render(request, 'new_osn-input.html', context)


@login_required(login_url='/login/')
def siswa_osn_delete(request, slug, pk):

    data = get_object_or_404(SiswaOSN, bidang_osn__slug=slug, nama_siswa_id=pk)

    if request.method == "POST":
        data.delete()
        return redirect('osn:detail-bidang-osn', slug)

    context = {
        'data': data,
    }
    return render(request, 'new_osn-delete.html', context)


@login_required(login_url='/login/')
def laporan_osn_input(request, slug):
    siswa_osn = SiswaOSN.objects.filter(bidang_osn__slug=slug)
    if request.method == "POST":
        forms = FormInputLaporanOSN(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('osn:detail-bidang-osn', slug)
        else:
            forms = FormInputLaporanOSN(request.POST, request.FILES)
            messages.error(request, "Yang kamu isi ada yang salah. Mohon cek ulang.")
    else:
        forms = FormInputLaporanOSN()
    context = {
        'forms': forms,
        'slug': slug,
        'name': "Input Laporan OSN",
        'siswa_osn': siswa_osn,
    }
    return render(request, 'new_osn-input.html', context)



@login_required(login_url='/login/')
def laporan_osn_edit(request, slug, pk):

    data = get_object_or_404(LaporanOSN, bidang_osn__slug=slug, id=pk)

    if request.method == "POST":
        forms = FormEditLaporanOSN(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            return redirect('osn:detail-bidang-osn', slug)
        else:
            forms = FormEditLaporanOSN(instance=data)
            messages.error(request, "Yang kamu isi ada yang salah. Mohon cek ulang.")
    else:
        forms = FormEditLaporanOSN(instance=data)
    context = {
        'forms': forms,
        'slug': slug,
        'name': "Edit Laporan OSN",
    }
    return render(request, 'new_osn-input.html', context)


@login_required(login_url='/login/')
def laporan_osn_delete(request, slug, pk):

    data = get_object_or_404(LaporanOSN, bidang_osn__slug=slug, id=pk)

    if request.method == "POST":
        data.delete()
        return redirect('osn:detail-bidang-osn', slug)

    context = {
        'data': data,
    }
    return render(request, 'new_osn-delete.html', context)


def cetak_laporan_osnk(request, slug):
    locale.setlocale(locale.LC_ALL, 'id_ID')
    tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
    data = get_object_or_404(BidangOSN, slug=slug)
    data_siswa = SiswaOSN.objects.filter(bidang_osn__slug=slug).order_by('nama_siswa__kelas', 'nama_siswa__nama')
    data_laporan = LaporanOSN.objects.filter(bidang_osn__nama_bidang=data.nama_bidang).filter(tanggal_pembinaan__lt="2023-04-07").order_by('tanggal_pembinaan')
    # angka = [x for x in range(15)]
    context = {
        # 'angka': angka,
        'level': "KABUPATEN",
        'tag': "OSN-K",
        'data': data,
        'data_siswa': data_siswa,
        'data_laporan': data_laporan,
        'tanggal': tanggal,
    }
    return render(request, 'osn-print.html', context)

def cetak_laporan_osnp(request, slug):
    locale.setlocale(locale.LC_ALL, 'id_ID')
    tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
    data = get_object_or_404(BidangOSN, slug=slug)
    data_siswa = SiswaOSN.objects.filter(bidang_osn__slug=slug).order_by('nama_siswa__kelas', 'nama_siswa__nama')
    data_laporan = LaporanOSN.objects.filter(bidang_osn__nama_bidang=data.nama_bidang).filter(tanggal_pembinaan__gt="2023-04-06").filter(tanggal_pembinaan__lt="2023-06-09").order_by('tanggal_pembinaan')
    # angka = [x for x in range(15)]
    context = {
        'level': "PROVINSI",
        'tag': "OSN-P",
        'data': data,
        'data_siswa': data_siswa,
        'data_laporan': data_laporan,
        'tanggal': tanggal,
    }
    return render(request, 'osn-print.html', context)
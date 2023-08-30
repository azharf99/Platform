from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from prestasi.forms import PrestasiInputForm, PrestasiEditForm, DokumentasiPrestasiEditForm, DokumentasiPrestasiInputForm
from prestasi.models import Prestasi, DokumentasiPrestasi
from django.contrib import messages

from userlog.models import UserLog
from io import BytesIO

import xlsxwriter


# Create your views here.
class PrestasiIndexView(ListView):
    model = Prestasi
    queryset = Prestasi.objects.all().order_by('-tahun_lomba', 'peraih_prestasi')
    paginate_by = 9
    template_name = 'prestasi2.html'


def index(request):
    prestasi = Prestasi.objects.all().order_by('-tahun_lomba', 'peraih_prestasi')
    context = {
        'prestasi': prestasi
    }
    return render(request, 'prestasi.html', context)


def prestasi_detail(request, pk):
    data = get_object_or_404(Prestasi, id=pk)
    context = {
        'data': data,
    }
    return render(request, 'prestasi-detail.html', context)


def print_to_excel(request):
    nilai = Prestasi.objects.all().order_by('-tahun_lomba',
                                             'peraih_prestasi')
    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ['No', 'Peraih Prestasi', 'Kelas', 'Kategori Lomba', 'Jenis Lomba', 'Tingkat Lomba', 'Tahun Lomba', 'Nama Lomba', 'Bidang Lomba', 'Predikat', 'Penyelengggara', 'Sekolah'])
    row = 1
    col = 0
    for data in nilai:
        worksheet.write_row(row, col, [row, data.peraih_prestasi, data.kelas_peraih_prestasi, data.kategori, data.jenis_lomba, data.tingkat_lomba, data.tahun_lomba, data.nama_lomba, data.bidang_lomba, data.kategori_kemenangan, data.Penyelenggara_lomba, data.sekolah])
        row += 1
    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='Prestasi SMA IT Al Binaa.xlsx')

@login_required(login_url="/login/")
def prestasi_input(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        data = request.POST.get('nama_lomba')
        forms = PrestasiInputForm(request.POST, request.FILES)
        if forms.is_valid():
            f = forms.save()
            DokumentasiPrestasi.objects.create(
                prestasi=f,
            )
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="ADD",
                app="PRESTASI",
                message="Berhasil menambahkan data prestasi {}".format(data)
            )
            return redirect('prestasi:prestasi-index')
        else:
            forms = PrestasiInputForm(request.POST, request.FILES)
            messages.error(request, "Yang kamu isi ada yang salah dalam isiannya. Tolong diperiksa lagi.")
    else:
        forms = PrestasiInputForm()

    context = {
        'forms': forms,
    }
    return render(request, 'prestasi-input.html', context)


@login_required(login_url="/login/")
def prestasi_edit(request, pk):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    data = get_object_or_404(Prestasi, id=pk)
    if request.method == 'POST':
        forms = PrestasiEditForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="PRESTASI",
                message="Berhasil mengubah data prestasi {}".format(data)
            )
            return redirect('prestasi:prestasi-index')
        else:
            forms = PrestasiEditForm(request.POST)
            messages.error(request, "Yang kamu isi ada yang salah dalam isiannya. Tolong diperiksa lagi.")
    else:
        forms = PrestasiEditForm(instance=data)

    context = {
        'forms': forms,
    }
    return render(request, 'prestasi-input.html', context)


@login_required(login_url="/login/")
def prestasi_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    data = get_object_or_404(Prestasi, id=pk)
    if request.method == 'POST':
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DELETE",
            app="PRESTASI",
            message="Berhasil menghapus data prestasi {}".format(data)
        )
        data.delete()
        return redirect('prestasi:prestasi-index')

    context = {
        'data': data,
    }
    return render(request, 'prestasi-delete.html', context)


def dokumentasi_prestasi_detail(request, pk):
    data = get_object_or_404(DokumentasiPrestasi, prestasi_id=pk)
    context = {
        'data': data,
    }
    return render(request, 'prestasi-foto-detail.html', context)

@login_required(login_url="/login/")
def dokumentasi_prestasi_input(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        data = request.POST.get('prestasi')
        forms = DokumentasiPrestasiInputForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="ADD",
                app="PRESTASI_DOKUMENTASI",
                message="Berhasil menambahkan foto/dokumentasi prestasi dengan id {}".format(data)
            )
            return redirect('prestasi:prestasi-index')
        else:
            forms = DokumentasiPrestasiInputForm(request.POST, request.FILES)
            messages.error(request, "Yang kamu isi ada yang salah dalam isiannya. Tolong diperiksa lagi.")
    else:
        forms = DokumentasiPrestasiInputForm()

    context = {
        'forms': forms,
    }
    return render(request, 'prestasi-foto-input.html', context)


@login_required(login_url="/login/")
def dokumentasi_prestasi_edit(request, pk):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    data = get_object_or_404(DokumentasiPrestasi, id=pk)
    if request.method == 'POST':
        forms = DokumentasiPrestasiEditForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="PRESTASI_DOKUMENTASI",
                message="Berhasil mengubah foto/dokumentasi prestasi {}".format(data)
            )
            return redirect('prestasi:prestasi-index')
        else:
            forms = DokumentasiPrestasiEditForm(request.POST, request.FILES)
            messages.error(request, "Yang kamu isi ada yang salah dalam isiannya. Tolong diperiksa lagi.")
    else:
        forms = DokumentasiPrestasiEditForm(instance=data)

    context = {
        'forms': forms,
    }
    return render(request, 'prestasi-foto-input.html', context)


@login_required(login_url="/login/")
def dokumentasi_prestasi_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    data = get_object_or_404(DokumentasiPrestasi, id=pk)
    if request.method == 'POST':
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DELETE",
            app="PRESTASI_DOKUMENTASI",
            message="Berhasil menghapus foto/dokumentasi prestasi {}".format(data)
        )
        data.delete()
        return redirect('prestasi:prestasi-index')

    context = {
        'data': data,
    }
    return render(request, 'prestasi-foto-delete.html', context)

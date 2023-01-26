from io import BytesIO

import xlsxwriter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse

from ekskul.models import Extracurricular, StudentOrganization
from nilai.forms import NilaiForm, NilaiEditForm
from nilai.models import Penilaian
from userlog.models import UserLog


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
    return render(request, 'nilai.html', context)


def nilai_detail(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    nilai = Penilaian.objects.filter(siswa__ekskul_siswa__slug=slug)
    forms = NilaiForm()
    context = {
        'ekskul': ekskul,
        'nilai': nilai,
        'forms': forms,
    }
    return render(request, 'nilai-detail.html', context)


def nilai_kelas_view(request):
    nilai = Penilaian.objects.all().order_by('siswa__nama_siswa__kelas',
                                             'siswa__ekskul_siswa__nama')
    context = {
        'nilai': nilai,
    }
    return render(request, 'nilai-berdasarkan-kelas.html', context)


@login_required(login_url='/login/')
def print_to_excel(request):
    nilai = Penilaian.objects.all().order_by('siswa__nama_siswa__kelas',
                                             'siswa__ekskul_siswa__nama')
    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ['No', 'Ekskul', 'Nama Santri', 'Kelas', 'Nilai'])
    row = 1
    col = 0
    for data in nilai:
        worksheet.write_row(row, col, [row, data.siswa.ekskul_siswa.nama, data.siswa.nama_siswa.nama, data.siswa.nama_siswa.kelas, data.nilai])
        row += 1
    workbook.close()
    buffer.seek(0)
    UserLog.objects.create(
        user=request.user.teacher,
        action_flag="PRINT",
        app="NILAI",
        message="Berhasil download data nilai semua ekskul/sc dalam format Excel"
    )
    return FileResponse(buffer, as_attachment=True, filename='Nilai Ekskul SMA IT Al Binaa.xlsx')

@login_required(login_url='/login/')
def nilai_input(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    siswa = StudentOrganization.objects.filter(ekskul_siswa__slug=slug)
    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if request.user.id not in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    if request.method == "POST":
        id_siswa = request.POST.get('siswa')
        try:
            Penilaian.objects.get(siswa_id=id_siswa)
            forms = NilaiForm(request.POST)
            messages.error(request,
                           "Maaf, nilai siswa tersebut sudah ada. Jika ingin mengubahnya, silahkan gunakan fitur edit nilai")
        except:
            forms = NilaiForm(request.POST)
            forms.siswa = id_siswa
            if forms.is_valid():
                forms.save()
                data = Penilaian.objects.get(siswa_id=id_siswa)
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="ADD",
                    app="NILAI",
                    message="Berhasil menambahkan data nilai ekskul {} atas nama {}".format(ekskul, data.siswa.nama_siswa.nama)
                )
                return redirect('nilai:nilai-detail', ekskul.slug)
            else:
                messages.error(request, "Isi data dengan benar!")

    else:
        forms = NilaiForm()
    context = {
        'ekskul': ekskul,
        'siswa': siswa,
        'forms': forms,
    }
    return render(request, 'nilai-input.html', context)


@login_required(login_url='/login/')
def nilai_edit(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    nilai = Penilaian.objects.get(id=pk)
    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if request.user.id not in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    if request.method == "POST":
        forms = NilaiEditForm(request.POST, instance=nilai)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="NILAI",
                message="Berhasil mengubah data nilai ekskul {} atas nama {}".format(ekskul, nilai.siswa.nama_siswa.nama)
            )
            return redirect('nilai:nilai-detail', ekskul.slug)
        else:
            forms = NilaiEditForm(instance=nilai)
            messages.error(request, "Isi data dengan benar!")
    else:
        forms = NilaiEditForm(instance=nilai)

    context = {
        'ekskul': ekskul,
        'forms': forms,
        'nilai': nilai,
    }
    return render(request, 'nilai-edit.html', context)


@login_required(login_url='/login/')
def nilai_delete(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if request.user.id not in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    data = Penilaian.objects.get(id=pk)
    if request.method == "POST":
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DELETE",
            app="NILAI",
            message="Berhasil menghapus data nilai ekskul {} atas nama {}".format(ekskul, data.siswa.nama_siswa.nama)
        )
        data.delete()
        return redirect('nilai:nilai-detail', ekskul.slug)
    context = {
        'ekskul': ekskul,
        'data': data,
    }
    return render(request, 'nilai-delete.html', context)


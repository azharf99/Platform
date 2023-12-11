from io import BytesIO

import xlsxwriter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.views.generic import ListView

from ekskul.models import Extracurricular, StudentOrganization
from nilai.forms import NilaiForm, NilaiEditForm
from nilai.models import Penilaian
from userlog.models import UserLog
from dashboard.whatsapp import send_whatsapp_input_anggota


# Create your views here.

class NilaiIndexView(ListView):
    model = Extracurricular
    template_name = 'new_nilai.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return Extracurricular.objects.all().order_by('tipe', 'nama_ekskul')
            else:
                return Extracurricular.objects.filter(pembina=self.request.user.teacher).order_by('tipe', 'nama_ekskul')
        else:
            return Extracurricular.objects.all().order_by('tipe', 'nama_ekskul')


def nilai_detail(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    nilai = Penilaian.objects.filter(siswa__ekskul__slug=slug)
    forms = NilaiForm()
    context = {
        'ekskul': ekskul,
        'nilai': nilai,
        'forms': forms,
    }
    return render(request, 'new_nilai-detail.html', context)


def nilai_kelas_view(request):
    nilai = Penilaian.objects.all().order_by('siswa__siswa__kelas', 'siswa__siswa__nama_siswa',
                                             'siswa__ekskul__nama_ekskul')
    context = {
        'nilai': nilai,
    }
    return render(request, 'new_nilai-list.html', context)

@login_required(login_url='/login/')
def print_to_excel(request):
    nilai = Penilaian.objects.all().order_by('siswa__siswa__kelas', 'siswa__siswa__nama_siswa',
                                             'siswa__ekskul__nama_ekskul')
    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ['No', 'Ekskul', 'Nama Santri', 'Kelas', 'Nilai'])
    row = 1
    col = 0
    for data in nilai:
        worksheet.write_row(row, col, [row, data.siswa.ekskul.nama_ekskul, data.siswa.siswa.nama_siswa, data.siswa.siswa.kelas, data.nilai])
        row += 1
    workbook.close()
    buffer.seek(0)

    UserLog.objects.create(
        user=request.user.teacher,
        action_flag="PRINT",
        app="NILAI",
        message="Berhasil download data nilai semua ekskul/sc dalam format Excel"
    )
    send_whatsapp_input_anggota(request.user.teacher.no_hp, 'ekskul/SC', 'Nilai', 'nilai', 'download')

    return FileResponse(buffer, as_attachment=True, filename='Nilai Ekskul SMA IT Al Binaa.xlsx')

@login_required(login_url='/login/')
def nilai_input(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    siswa = StudentOrganization.objects.filter(ekskul__slug=slug)
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
                messages.success(request, "Input nilai berhasil!")
                data = Penilaian.objects.get(siswa_id=id_siswa)
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="ADD",
                    app="NILAI",
                    message="Berhasil menambahkan data nilai ekskul {} atas nama {}".format(ekskul, data.siswa.siswa.nama_siswa)
                )
                send_whatsapp_input_anggota(request.user.teacher.no_hp, data.siswa.siswa.nama_siswa, f'Nilai {ekskul}', f'nilai/{ekskul.slug}', 'input')
                return redirect('nilai:nilai-input', ekskul.slug)
            else:
                messages.error(request, "Isi data dengan benar!")

    else:
        forms = NilaiForm()
    context = {
        'ekskul': ekskul,
        'siswa': siswa,
        'forms': forms,
        'edit' : False,
    }
    return render(request, 'new_nilai-input.html', context)


@login_required(login_url='/login/')
def nilai_edit(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    siswa = Penilaian.objects.get(id=pk)
    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if request.user.id not in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    if request.method == "POST":
        forms = NilaiEditForm(request.POST, instance=siswa)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="NILAI",
                message="Berhasil mengubah data nilai ekskul {} atas nama {}".format(ekskul, siswa.siswa.siswa.nama_siswa)
            )
            send_whatsapp_input_anggota(request.user.teacher.no_hp, siswa.siswa.siswa.nama_siswa, f'Nilai {ekskul}', f'nilai/{ekskul.slug}', 'mengubah')
            return redirect('nilai:nilai-detail', ekskul.slug)
        else:
            forms = NilaiEditForm(instance=siswa)
            messages.error(request, "Isi data dengan benar!")
    else:
        forms = NilaiEditForm(instance=siswa)

    context = {
        'ekskul': ekskul,
        'forms': forms,
        'siswa': siswa,
        'edit' : True,

    }
    return render(request, 'new_nilai-input.html', context)


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
            message="Berhasil menghapus data nilai ekskul {} atas nama {}".format(ekskul, data.siswa.siswa.nama_siswa)
        )
        send_whatsapp_input_anggota(request.user.teacher.no_hp, data.siswa.siswa.nama_siswa, f'Nilai {ekskul}', f'nilai/{ekskul.slug}', 'menghapus')
        data.delete()
        return redirect('nilai:nilai-detail', ekskul.slug)
    context = {
        'ekskul': ekskul,
        'data': data,
    }
    return render(request, 'new_nilai-delete.html', context)


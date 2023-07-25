import datetime
import locale

import requests

import pytz
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import ListView, DetailView

from laporan.models import Report
from laporan.forms import FormLaporanKehadiran
from ekskul.models import Extracurricular, StudentOrganization, Teacher
from userlog.models import UserLog


class LaporanIndexView(ListView):
    model = Extracurricular
    template_name = 'laporan.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return Extracurricular.objects.all().order_by('tipe', 'nama_ekskul')
            else:
                return Extracurricular.objects.filter(pembina=self.request.user.teacher).order_by('tipe', 'nama_ekskul')
        else:
            return Extracurricular.objects.all().order_by('tipe', 'nama_ekskul')

# class PrintToPDFView(DetailView):
#     model = Report
#     template_name = 'laporan-print.html'

    # def get_queryset(self):
    #     if datetime.date.today().month > 1:
    #         return Report.objects.filter(nama_ekskul_id=self.kwargs['pk'],
    #                                      tanggal_pembinaan__month=7).order_by(
    #             'tanggal_pembinaan')
    #     else:
    #         return Report.objects.filter(nama_ekskul_id=self.kwargs['pk'],
    #                                      tanggal_pembinaan__month=datetime.date.today().month).order_by(
    #             'tanggal_pembinaan')

    # def get_object(self):
    #     course = get_object_or_404(Report, pk=self.kwargs['pk'])
    #     return self.model.objects.filter(nama_ekskul__slug=slug)
    # def get_context_data(self, **kwargs):
    #     context = super(PrintToPDFView, self).get_context_data(**kwargs)
    #     context['tanggal'] = timezone.now()
    #     # context['students'] = StudentOrganization.objects.filter(ekskul__slug=self.kwargs['slug']).order_by('siswa__kelas', 'siswa__nama_siswa')
    #     return context


@login_required(login_url='/login/')
def print_to_pdf(request, slug):
    locale.setlocale(locale.LC_ALL, 'id_ID')
    tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
    if datetime.date.today().month > 1:
        reports = Report.objects.filter(nama_ekskul__slug=slug, tanggal_pembinaan__month=(datetime.date.today().month)).order_by('tanggal_pembinaan')
    else:
        reports = Report.objects.filter(nama_ekskul__slug=slug, tanggal_pembinaan__month=datetime.date.today().month).order_by('tanggal_pembinaan')
    students = StudentOrganization.objects.filter(ekskul__slug=slug).order_by('siswa__kelas', 'siswa__nama_siswa')
    angka = [x for x in range(15)]
    context = {
        'reports': reports,
        'angka': angka,
        'students': students,
        'tanggal': tanggal,
    }

    return render(request, 'laporan-print.html', context)

def laporan_ekskul_print_versi2(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    filtered_report = Report.objects.filter(nama_ekskul__slug=slug).order_by('tanggal_pembinaan')
    context = {
        'ekskul': ekskul,
        'filtered_report': filtered_report,
    }
    return render(request, 'laporan-print2.html', context)

class LaporanEkskulView(ListView):
    model = Report
    template_name = 'laporan-ekskul2.html'
    queryset = Report.objects.all()
    paginate_by = 10

    def get_queryset(self):
        return self.queryset.filter(nama_ekskul__slug=self.kwargs.get('slug')).order_by('-tanggal_pembinaan')

def laporan_ekskul(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    bulan_ini = datetime.date.today().__format__("%B %Y")
    teachers = Teacher.objects.filter(extracurricular=ekskul)
    all = teachers.values_list('user_id', flat=True)
    filtered_report = Report.objects.filter(nama_ekskul__slug=slug).filter(
        tanggal_pembinaan__month=datetime.date.today().month).order_by('tanggal_pembinaan')
    if request.method == "POST":
        bulan = request.POST.get("bulan")
        if bulan != 0:
            filtered_report = Report.objects.filter(nama_ekskul__slug=slug).filter(
                tanggal_pembinaan__month=bulan).order_by('tanggal_pembinaan')
            bulan_ini = None
        else:
            filtered_report = Report.objects.filter(nama_ekskul__slug=slug).filter(
                tanggal_pembinaan__month=datetime.date.today().month).order_by('tanggal_pembinaan')

    # else:
    #     filtered_report = Report.objects.filter(nama_ekskul__slug=slug).order_by('tanggal_pembinaan')

    if request.user.is_authenticated:
        if not request.user.id in all and not request.user.is_superuser:
            # if not request.user.teacher == ekskul.pembina and not request.user.is_superuser:
            context = {
                'ekskul': ekskul,
                'filtered_report': filtered_report,
                'bulan_ini': bulan_ini,
                'display': None,
            }
        else:
            context = {
                'ekskul': ekskul,
                'filtered_report': filtered_report,
                'bulan_ini': bulan_ini,
                'display': True,
            }
    else:
        context = {
            'ekskul': ekskul,
            'filtered_report': filtered_report,
            'bulan_ini': bulan_ini,
            'display': None
        }
    return render(request, 'laporan-ekskul.html', context)


class LaporanDetailView(DetailView):
    model = Report
    template_name = 'laporan-detail.html'


@login_required(login_url='/login/')
def laporan_input(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    filtered_student = StudentOrganization.objects.filter(ekskul__slug=slug)
    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if request.user.id not in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    nama_ekskul = request.POST.get('nama_ekskul')
    tanggal_pembinaan = request.POST.get('tanggal_pembinaan')
    kehadiran_santri = request.POST.get('kehadiran_santri')
    pembina = request.POST.get('pembina_ekskul')
    image = request.FILES.get('foto')

    if request.method == 'POST':
        try:
            Report.objects.get(tanggal_pembinaan=tanggal_pembinaan, nama_ekskul__slug=slug)
            form = FormLaporanKehadiran(request.POST, request.FILES)
            messages.error(request, "Laporan untuk tanggal ini sudah ada. Silahkan pilih tanggal lain")
        except:
            form = FormLaporanKehadiran(request.POST, request.FILES)
            FormLaporanKehadiran.nama_ekskul = nama_ekskul
            FormLaporanKehadiran.tanggal_pembinaan = tanggal_pembinaan
            FormLaporanKehadiran.kehadiran_santri = kehadiran_santri
            FormLaporanKehadiran.pembina_ekskul = pembina
            FormLaporanKehadiran.foto = image
            if form.is_valid():
                form.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="ADD",
                    app="LAPORAN",
                    message="Berhasil menambahkan data laporan pertemuan ekskul {} untuk tanggal {}".format(ekskul,
                                                                                                            tanggal_pembinaan)
                )

                token = settings.TOKEN
                phone = "62%s" % request.user.teacher.no_hp
                message = '''*[NOTIFIKASI]*
Assalamu'alaikum %s, Anda berhasil input laporan pertemuan ekskul *%s* untuk tanggal *%s*.
Detail laporan:
https://ekskul.smasitalbinaa.com/laporan/%s

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, ekskul.nama_ekskul, tanggal_pembinaan, ekskul.slug)
                url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"

                response = requests.get(url)
                result = response.text
                print(result)

                return redirect('laporan:laporan-ekskul', ekskul.slug)

    else:
        form = FormLaporanKehadiran()

    context = {
        'ekskul': ekskul,
        'filtered_student': filtered_student,
        'form': form,
    }
    return render(request, 'laporan-input.html', context)

#
# @login_required(login_url='/login/')
# def laporan_upload(request, slug):
#     ekskul = get_object_or_404(Extracurricular, slug=slug)
#     filtered_report = Report.objects.filter(nama_ekskul__slug=slug).order_by('-tanggal_pembinaan')
#     all = ekskul.pembina.all().values_list('user_id', flat=True)
#     if request.user.id not in all and not request.user.is_superuser:
#         return HttpResponseRedirect(reverse('restricted'))
#
#     if request.method == 'POST':
#         id_laporan = request.POST.get('laporan')
#         laporan = get_object_or_404(Report, id=id_laporan)
#         try:
#             UploadImage.objects.get(laporan_id=id_laporan)
#             forms = FormUploadLaporanKehadiran(request.POST)
#             messages.error(request, "Dokumentasi/Foto untuk laporan ini sudah ada. Silahkan pilih laporan lain")
#         except:
#             image = request.FILES.get('foto_absensi')
#
#             UploadImage.objects.create(
#                 laporan=laporan,
#                 foto_absensi=image
#             )
#             UserLog.objects.create(
#                 user=request.user.teacher,
#                 action_flag="ADD",
#                 app="LAPORAN_FOTO",
#                 message="Berhasil mengupload foto pertemuan ekskul {} untuk tanggal {}".format(ekskul,
#                                                                                                laporan.tanggal_pembinaan)
#             )
#
#             token = settings.TOKEN
#             phone = "62%s" % request.user.teacher.no_hp
#             message = '''*[NOTIFIKASI]*
# Assalamu'alaikum %s, Anda berhasil upload foto pertemuan ekskul %s untuk laporan *%s*.
# Detail laporan:
# https://ekskul.smasitalbinaa.com/laporan/%s
#
# Syukron.
#
# _Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, ekskul.nama_ekskul, laporan, ekskul.slug)
#             url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={token}"
#
#             response = requests.get(url)
#             result = response.text
#             print(result)
#
#             return redirect('laporan:laporan-ekskul', ekskul.slug)
#     else:
#         forms = FormUploadLaporanKehadiran()
#
#     context = {
#         'ekskul': ekskul,
#         'filtered_report': filtered_report,
#         'forms': forms,
#     }
#     return render(request, 'laporan-upload.html', context)


@login_required(login_url='/login/')
def laporan_edit(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    laporan = get_object_or_404(Report, nama_ekskul__slug=slug, id=pk)
    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if request.user.id not in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    if request.method == 'POST':
        form = FormLaporanKehadiran(request.POST, request.FILES, instance=laporan)
        if form.is_valid():
            form.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="LAPORAN",
                message="Berhasil mengubah data laporan pertemuan ekskul {} untuk tanggal {}".format(ekskul,
                                                                                                     laporan.tanggal_pembinaan)
            )

            url = 'https://api.watsap.id/send-message'
            data_post = {
                'id_device': settings.ID_DEVICE,
                'api-key': settings.API_KEY,
                'no_hp': '0%s' % request.user.teacher.no_hp,
                'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, Anda berhasil mengubah data laporan pertemuan ekskul %s untuk tanggal *%s*.
Detail laporan:
https://ekskul.smasitalbinaa.com/laporan/%s

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, ekskul.nama, laporan.tanggal_pembinaan, ekskul.slug)
            }
            headers = {'Content-Type': 'application/json'}
            requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)

            return redirect('laporan:laporan-ekskul', ekskul.slug)
        else:
            messages.error(request, "Mohon input data dengan benar!")
            form = FormLaporanKehadiran(request.POST, instance=laporan)
    else:
        form = FormLaporanKehadiran(instance=laporan)
    context = {
        'ekskul': ekskul,
        'form': form,
    }
    return render(request, 'laporan-edit.html', context)


@login_required(login_url='/login/')
def laporan_delete(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    laporan = get_object_or_404(Report, nama_ekskul__slug=slug, id=pk)
    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if request.user.id not in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    if request.method == 'POST':
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DELETE",
            app="LAPORAN",
            message="Berhasil menghapus data laporan pertemuan ekskul {} untuk tanggal {}".format(ekskul,
                                                                                                  laporan.tanggal_pembinaan)
        )

        url = 'https://api.watsap.id/send-message'
        data_post = {
            'id_device': settings.ID_DEVICE,
            'api-key': settings.API_KEY,
            'no_hp': '0%s' % request.user.teacher.no_hp,
            'pesan': '''*[NOTIFIKASI]*
Assalamu'alaikum %s, Anda berhasil menghapus laporan pertemuan ekskul %s untuk tanggal *%s*.
Detail laporan:
https://ekskul.smasitalbinaa.com/laporan/%s

Syukron.

_Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, ekskul.nama, laporan.tanggal_pembinaan, ekskul.slug)
        }
        headers = {'Content-Type': 'application/json'}
        requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)

        laporan.delete()
        return redirect('laporan:laporan-ekskul', ekskul.slug)
    context = {
        'ekskul': ekskul,
        'laporan': laporan,
    }

    return render(request, 'laporan-delete.html', context)

#
# @login_required(login_url='/login/')
# def laporan_upload_edit(request, slug, pk):
#     ekskul = get_object_or_404(Extracurricular, slug=slug)
#     laporan = get_object_or_404(Report, id=pk)
#     foto = UploadImage.objects.get(laporan_id=laporan.id)
#     all = ekskul.pembina.all().values_list('user_id', flat=True)
#     if not request.user.id in all and not request.user.is_superuser:
#         return HttpResponseRedirect(reverse('restricted'))
#
#     if request.method == 'POST':
#         form_upload_edit = FormEditUploadLaporanKehadiran(request.POST, request.FILES, instance=foto)
#         if form_upload_edit.is_valid():
#             form_upload_edit.save()
#             UserLog.objects.create(
#                 user=request.user.teacher,
#                 action_flag="CHANGE",
#                 app="LAPORAN_FOTO",
#                 message="Berhasil mengubah foto laporan pertemuan ekskul {} untuk tanggal {}".format(ekskul,
#                                                                                                      laporan.tanggal_pembinaan)
#             )
#
#             url = 'https://api.watsap.id/send-message'
#             data_post = {
#                 'id_device': settings.ID_DEVICE,
#                 'api-key': settings.API_KEY,
#                 'no_hp': '0%s' % request.user.teacher.no_hp,
#                 'pesan': '''*[NOTIFIKASI]*
# Assalamu'alaikum %s, Anda berhasil mengubah foto pertemuan ekskul %s untuk tanggal *%s*.
# Detail laporan:
# https://ekskul.smasitalbinaa.com/laporan/%s
#
# Syukron.
#
# _Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, ekskul.nama, laporan.tanggal_pembinaan, ekskul.slug)
#             }
#             headers = {'Content-Type': 'application/json'}
#             requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)
#
#             return redirect('laporan:laporan-ekskul', ekskul.slug)
#         else:
#             messages.error(request, "Mohon input data dengan benar!")
#             form_upload_edit = FormEditUploadLaporanKehadiran(request.POST, request.FILES, instance=foto)
#     else:
#         form_upload_edit = FormEditUploadLaporanKehadiran(instance=foto)
#
#     context = {
#         'ekskul': ekskul,
#         'form_upload_edit': form_upload_edit,
#     }
#     return render(request, 'laporan-upload-edit.html', context)
#
#
# @login_required(login_url='/login/')
# def laporan_upload_delete(request, slug, pk):
#     ekskul = get_object_or_404(Extracurricular, slug=slug)
#     laporan = get_object_or_404(Report, id=pk)
#     foto = UploadImage.objects.get(laporan_id=laporan.id)
#     all = ekskul.pembina.all().values_list('user_id', flat=True)
#     if request.user.id not in all and not request.user.is_superuser:
#         return HttpResponseRedirect(reverse('restricted'))
#
#     if request.method == 'POST':
#         UserLog.objects.create(
#             user=request.user.teacher,
#             action_flag="DELETE",
#             app="LAPORAN_FOTO",
#             message="Berhasil menghapus foto laporan pertemuan ekskul {} untuk tanggal {}".format(ekskul,
#                                                                                                   laporan.tanggal_pembinaan)
#         )
#
#         url = 'https://api.watsap.id/send-message'
#         data_post = {
#             'id_device': settings.ID_DEVICE,
#             'api-key': settings.API_KEY,
#             'no_hp': '0%s' % request.user.teacher.no_hp,
#             'pesan': '''*[NOTIFIKASI]*
# Assalamu'alaikum %s, Anda berhasil menghapus foto pertemuan ekskul %s untuk tanggal *%s*.
# Detail laporan:
# https://ekskul.smasitalbinaa.com/laporan/%s
#
# Syukron.
#
# _Ini adalah pesan otomatis, jangan dibalas._''' % (request.user.teacher, ekskul.nama, laporan.tanggal_pembinaan, ekskul.slug)
#         }
#         headers = {'Content-Type': 'application/json'}
#         requests.post(url, json=data_post, headers=headers, allow_redirects=True, verify=False)
#
#         foto.delete()
#         return redirect('laporan:laporan-ekskul', ekskul.slug)
#
#     context = {
#         'ekskul': ekskul,
#         'foto': foto,
#     }
#
#     return render(request, 'laporan-upload-delete.html', context)

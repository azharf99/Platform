from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from ekskul.models import Extracurricular, Student, StudentOrganization, Teacher, User
from laporan.models import Report
from ekskul.forms import InputAnggotaEkskulForm, PembinaEkskulForm, EkskulForm, CustomUserCreationForm, UsernameChangeForm, CustomPasswordChangeForm
from userlog.models import UserLog
from django.views.decorators.csrf import csrf_protect

# Create your views here.

def home(request):
    if request.user.is_authenticated or request.user.is_superuser:
        data = Extracurricular.objects.filter(pembina=request.user.teacher).order_by('tipe', 'nama')
        extra = Extracurricular.objects.exclude(pembina=request.user.teacher).order_by('tipe', 'nama')
        context = {
            'data': data,
            'extra': extra,
        }
    else:
        data = Extracurricular.objects.all().order_by('tipe', 'nama')
        context = {
            'data': data,
        }

    return render(request, 'data.html', context)


def data_detail(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    teachers = Teacher.objects.filter(extracurricular=ekskul)
    filtered_students = Student.objects.filter(studentorganization__ekskul_siswa__nama=ekskul.nama).order_by('kelas',
                                                                                                             'nama')
    all = teachers.values_list('user_id', flat=True)
    if not request.user.id in all and not request.user.is_superuser:
        context = {
            'ekskul': ekskul,
            'teachers': teachers,
            'filtered_student': filtered_students,
            'pembina': False,
        }
    else:
        context = {
            'ekskul': ekskul,
            'teachers': teachers,
            'filtered_student': filtered_students,
            'pembina': True,
        }
    return render(request, 'data-detail.html', context)

def dokumentasi(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    filtered_report = Report.objects.filter(nama_ekskul__slug=slug).order_by('tanggal_pembinaan')
    context = {
        'ekskul': ekskul,
        'filtered_report': filtered_report,
    }
    return render(request, 'dokumentasi.html', context)


@login_required(login_url='/login/')
def input_anggota(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    all = ekskul.pembina.all().values_list('user_id', flat=True)
    student = Student.objects.all()
    if not request.user.id in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    data_ekskul = request.POST.get('ekskul_siswa')
    id_siswa = request.POST.get('nama_siswa')

    if request.method == 'POST':
        try:
            StudentOrganization.objects.get(nama_siswa_id=id_siswa, ekskul_siswa_id=data_ekskul)
            form = InputAnggotaEkskulForm(request.POST)
            messages.error(request, "Santri sudah ada di dalam anggota ekskul. Silahkan pilih santri lain")
        except:
            siswa = get_object_or_404(Student, id=id_siswa)
            form = InputAnggotaEkskulForm(request.POST)
            InputAnggotaEkskulForm.ekskul_siswa = data_ekskul
            InputAnggotaEkskulForm.nama_siswa = siswa
            if form.is_valid():
                form.save()
                messages.info(request, "Data Anggota Berhasil ditambahkan!")
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="ADD",
                    app="EKSKUL",
                    message="Berhasil menambahkan anggota baru ekskul {} atas nama {} kelas {}".format(ekskul, siswa.nama, siswa.kelas)
                )
                return redirect('ekskul:data-detail', ekskul.slug)
    else:
        form = InputAnggotaEkskulForm()
    context = {
        'ekskul': ekskul,
        'form': form,
        'student': student,

    }
    return render(request, 'input-anggota-ekskul.html', context)


@login_required(login_url='/login/')
def delete_anggota(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    deteled_student = get_object_or_404(StudentOrganization, ekskul_siswa__slug=slug, nama_siswa_id=pk)

    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if not request.user.id in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    if request.method == 'POST':
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DELETE",
            app="EKSKUL",
            message="Berhasil menghapus anggota ekskul {} atas nama {} kelas {}".format(ekskul, deteled_student.nama_siswa.nama, deteled_student.nama_siswa.kelas)
        )
        deteled_student.delete()
        return redirect('ekskul:data-detail', ekskul.slug)
    context = {
        'ekskul': ekskul,
        'deleted_student': deteled_student,
    }
    return render(request, 'delete-anggota.html', context)


@login_required(login_url='/login/')
def edit_ekskul(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)

    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if not request.user.id in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    if request.method == 'POST':
        form = EkskulForm(request.POST, instance=ekskul)
        if form.is_valid():
            form.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="EKSKUL",
                message="Berhasil mengedit data ekskul {}".format(ekskul)
            )
            return redirect('ekskul:data-detail', ekskul.slug)
    else:
        form = EkskulForm(instance=ekskul)
    context = {
        'ekskul': ekskul,
        'form': form,
    }
    return render(request, 'edit-ekskul.html', context)

@login_required(login_url='/login/')
def input_pembina(request):
    form = PembinaEkskulForm().as_p()
    return render(request, 'input-anggota-ekskul.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect("app-index")

    if request.method == "POST":
        username = request.POST.get('username').rstrip()
        password = request.POST.get('pass').rstrip()

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username tidak ada. anda perlu hubungi operator jika ingin mendaftar")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="LOGIN",
                app="EKSKUL",
                message="Berhasil melakukan login ke aplikasi"
            )
            return redirect('app-index')
        else:
            messages.warning(request, "Username atau Password salah!")
    context = {}
    return render(request, 'login.html', context)

@login_required(login_url='/login/')
def profil_view(request):
    if not request.user.teacher.nama_lengkap:
        redirect('edit-profil')
    try:
        user = request.user
        teacher = Teacher.objects.get(user_id=user.id)
        context = {
            'teacher': teacher,
        }
    except:
        return redirect('login')
    return render(request, 'profil.html', context)
@login_required(login_url='/login/')
def edit_profil_view(request):
    try:
        teacher = Teacher.objects.get(user_id=request.user.id)
        if request.method == "POST":
            form = PembinaEkskulForm(request.POST, request.FILES, instance=teacher)
            if form.is_valid():
                form.save()
                UserLog.objects.create(
                    user=request.user.teacher,
                    action_flag="CHANGE",
                    app="PROFILE",
                    message="Berhasil mengubah data diri di halaman profil",
                )
                return redirect('profil')
            else:
                messages.error(request, "Input data dengan benar!")
                form = PembinaEkskulForm(request.POST, request.FILES, instance=teacher)
        else:
            form = PembinaEkskulForm(instance=teacher)
        context = {
            'form': form,
        }
    except:
        return redirect('login')
    return render(request, 'profil-edit.html', context)


def logout_view(request):
    UserLog.objects.create(
        user=request.user.teacher,
        action_flag="LOGOUT",
        app="EKSKUL",
        message="Berhasil logout dari aplikasi",
    )
    logout(request)
    return redirect('app-index')


def register(request):
    if request.user.is_authenticated:
        return redirect('restricted')
    forms = CustomUserCreationForm()

    if request.method == "POST":
        forms = CustomUserCreationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password1')
        if forms.is_valid():
            forms.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            Teacher.objects.create(
                user_id=request.user.id,
                nama_lengkap="",
                niy=0,
                email="user@gmail.com",
                no_hp=0,
            )
            UserLog.objects.create(
                user="Pengguna ke-" + str(request.user.id),
                action_flag="ADD",
                app="PENGGUNA",
                message="Berhasil membuat akun baru di aplikasi ini",
            )
            return redirect('edit-profil')

    context = {
        'forms': forms,
    }
    return render(request, 'register.html', context)


# @login_required(login_url='/login')
def edit_username(request):
    if not request.user.is_authenticated:
        return redirect('restricted')
    forms = UsernameChangeForm(instance=request.user)

    if request.method == "POST":
        forms = UsernameChangeForm(request.POST, instance=request.user)
        if forms.is_valid():
            forms.save()
            return redirect('profil')

    context = {
        'forms': forms,
        'tipe' : 'change',
    }
    return render(request, 'register.html', context)

def edit_password(request):
    if not request.user.is_authenticated:
        return redirect('restricted')
    forms = CustomPasswordChangeForm(user=request.user)

    if request.method == "POST":
        password = request.POST.get('new_password1')
        forms = CustomPasswordChangeForm(request.user, request.POST)
        if forms.is_valid():
            forms.save()
            user = authenticate(request, username=request.user.username, password=password)
            login(request, user)
            return redirect('profil')

    context = {
        'forms': forms,
        'tipe' : 'change',
    }
    return render(request, 'register.html', context)
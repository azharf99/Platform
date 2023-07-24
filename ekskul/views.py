from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ekskul.models import Extracurricular, Student, StudentOrganization, Teacher, User
from ekskul.forms import InputAnggotaEkskulForm, PembinaEkskulForm, EkskulForm, CustomUserCreationForm, UsernameChangeForm, CustomPasswordChangeForm
from userlog.models import UserLog
from nilai.models import Penilaian
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView

# Create your views here.


class EkskulIndexView(ListView):
    model = Extracurricular

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return Extracurricular.objects.all().order_by('tipe', 'nama_ekskul')
            else:
                return Extracurricular.objects.filter(pembina=self.request.user.teacher).order_by('tipe', 'nama_ekskul')
        else:
            return Extracurricular.objects.all().order_by('tipe', 'nama_ekskul')


class EkskulDetailView(DetailView):
    model = Extracurricular



@login_required(login_url='/login/')
def input_anggota(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if not request.user.id in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))


    if request.method == 'POST':
        data_ekskul = request.POST.get('ekskul')
        id_siswa = request.POST.get('siswa')
        print(data_ekskul, id_siswa)
        try:
            ekskul = StudentOrganization.objects.get(siswa_id=id_siswa, ekskul_id=data_ekskul)
            form = InputAnggotaEkskulForm(request.POST)
            messages.error(request, "Santri sudah ada di dalam anggota ekskul. Silahkan pilih santri lain")
        except:
            # siswa = Student.objects.get(id=id_siswa)
            form = InputAnggotaEkskulForm(request.POST)
            if form.is_valid():
                messages.success(request, "Input data berhasil! Silahkan cek pada daftar yang ada")
                form.save()
                # data = StudentOrganization.objects.create(siswa_id=id_siswa, ekskul=ekskul)
                # data.save()
                # Penilaian.objects.create(
                #     siswa = ekskul,
                #     nilai = "A"
                #     )
                # UserLog.objects.create(
                #     user=request.user.teacher,
                #     action_flag="ADD",
                #     app="EKSKUL",
                #     message="Berhasil menambahkan anggota baru ekskul {} atas nama {} kelas {}".format(ekskul, siswa.nama_siswa, siswa.kelas)
                # )
                return redirect('ekskul:input-anggota', ekskul.slug)
    else:
        form = InputAnggotaEkskulForm()
    context = {
        'ekskul': ekskul,
        'form': form,

    }
    return render(request, 'input-anggota-ekskul.html', context)


@login_required(login_url='/login/')
def delete_anggota(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    deteled_student = get_object_or_404(StudentOrganization, siswa_id=pk, ekskul_id=ekskul.id)

    all = ekskul.pembina.all().values_list('user_id', flat=True)
    if not request.user.id in all and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))

    if request.method == 'POST':
        deteled_student.delete()
        # UserLog.objects.create(
        #     user=request.user.teacher,
        #     action_flag="DELETE",
        #     app="EKSKUL",
        #     message="Berhasil menghapus anggota ekskul {} atas nama {} kelas {}".format(ekskul, deteled_student.siswa.nama, deteled_student.siswa.kelas)
        # )
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
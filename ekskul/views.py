from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ekskul.models import Extracurricular, Student, StudentOrganization, Teacher, User
from ekskul.forms import InputAnggotaEkskulForm, PembinaEkskulForm, EkskulForm

# Create your views here.

def home(request):
    if request.GET.get('q') is not None or request.GET.get('q') == '':
        q = request.GET.get('q')
        data = Extracurricular.objects.filter(
        Q(nama__icontains=q)|Q(pembina__nama_lengkap__icontains=q)).order_by('tipe', 'nama')
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
    context = {
        'ekskul': ekskul,
        'teachers': teachers,
        'filtered_student': filtered_students,

    }
    return render(request, 'data-detail.html', context)


@login_required(login_url='/login/')
def input_anggota(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    for guru in ekskul.pembina.all():
        if not guru.user_id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))

    data_ekskul = request.POST.get('ekskul_siswa')
    id_siswa = request.POST.get('nama_siswa')

    if request.method == 'POST':
        try:
            siswa = StudentOrganization.objects.get(nama_siswa_id=id_siswa, ekskul_siswa_id=data_ekskul)
            form = InputAnggotaEkskulForm(request.POST)
            messages.error(request, "Santri sudah ada di dalam anggota ekskul. Silahkan pilih santri lain")
        except:
            form = InputAnggotaEkskulForm(request.POST)
            InputAnggotaEkskulForm.ekskul_siswa = data_ekskul
            if form.is_valid():
                form.save()
                return redirect('ekskul:data-detail', ekskul.slug)
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
    deteled_student = get_object_or_404(StudentOrganization, nama_siswa_id=pk, ekskul_siswa_id=ekskul.id)
    for guru in ekskul.pembina.all():
        if not guru.user_id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
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
    for guru in ekskul.pembina.all():
        if not guru.user_id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        form = EkskulForm(request.POST, instance=ekskul)
        if form.is_valid():
            form.save()
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


def login_view(request):
    if request.user.is_authenticated:
        return redirect("app-index")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username tidak ada. anda perlu hubungi operator jika ingin mendaftar")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
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
    logout(request)
    return redirect('app-index')
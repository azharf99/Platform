from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from ekskul.models import Extracurricular, Student, User, StudentOrganization
from ekskul.forms import InputAnggotaEkskulForm, InputPembinaEkskulForm, EkskulForm


# Create your views here.

def home(request):
    print(Extracurricular.objects.get(pembina__nama_id=request.user.teacher.id))
    data = Extracurricular.objects.all().order_by('tipe', 'nama')
    return render(request, 'data.html', context={'data': data})


# @login_required(login_url='/admin/login/')
def data_detail(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    teachers = User.objects.filter(teacher__extracurricular__slug=slug)
    filtered_students = Student.objects.filter(studentorganization__ekskul_siswa__nama=ekskul.nama).order_by('kelas', 'nama')
    context = {
        'ekskul': ekskul,
        'teachers': teachers,
        'filtered_student': filtered_students,

    }
    return render(request, 'data-detail.html', context)

@login_required(login_url='/admin/login')
def input_anggota(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    for guru in ekskul.pembina.all():
        if not guru.nama.id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        data_ekskul = request.POST.get('ekskul_siswa')
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

@login_required(login_url='/admin/login')
def delete_anggota(request, slug, pk):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    deteled_student = get_object_or_404(StudentOrganization, nama_siswa_id=pk)
    for guru in ekskul.pembina.all():
        if not guru.nama.id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        deteled_student.delete()
        return redirect('ekskul:data-detail', ekskul.slug)
    context = {
        'ekskul': ekskul,
        'deleted_student': deteled_student,
    }
    return render(request, 'delete-anggota.html', context)

@login_required(login_url='/admin/login')
def edit_ekskul(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    for guru in ekskul.pembina.all():
        if not guru.nama.id == request.user.id and not request.user.is_superuser:
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

def input_pembina(request):
    form = InputPembinaEkskulForm().as_p()
    return render(request, 'input-anggota-ekskul.html', {'form': form})



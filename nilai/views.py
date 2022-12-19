from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from ekskul.models import Extracurricular, StudentOrganization
from nilai.models import Penilaian
from nilai.forms import NilaiForm

# Create your views here.

def index(request):
    ekskul = Extracurricular.objects.all().order_by('tipe', 'nama')
    # nilai = Penilaian.objects.all().order_by('siswa__ekskul_siswa__nama','siswa__nama_siswa__kelas', 'siswa__nama_siswa__nama')
    context = {
        # 'nilai': nilai,
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

def nilai_input(request, slug):
    ekskul = get_object_or_404(Extracurricular, slug=slug)
    siswa = StudentOrganization.objects.filter(ekskul_siswa__slug=slug)
    for guru in ekskul.pembina.all():
        if not guru.nama.id == request.user.id and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
    if request.method == "POST":
        id_siswa = request.POST.get('siswa')
        forms = NilaiForm(request.POST)
        forms.siswa = id_siswa
        if forms.is_valid():
            forms.save()
            return redirect('nilai:nilai-detail', ekskul.slug)
    else:
        forms = NilaiForm()
    context = {
        'ekskul': ekskul,
        'siswa': siswa,
        'forms': forms,
    }
    return render(request, 'nilai-input.html', context)
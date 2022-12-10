from django.shortcuts import render, get_object_or_404
from ekskul.models import Extracurricular, Student, User

# Create your views here.

def home(request):
    ekskul = Extracurricular.objects.all().order_by('nama')
    return render(request, 'data.html', context={'data':ekskul})

def data_detail(request, pk):
    ekskul = Extracurricular.objects.get(id=pk)
    teacher = User.objects.get(teacher__extracurricular__nama=ekskul.nama)
    siswa = Student.objects.filter(ekskul=ekskul)

    return render(request, 'data-detail.html', context={'ekskul':ekskul, 'teacher':teacher, 'siswa':siswa})
from django.shortcuts import render
from django.db.models import Q
from deskripsi.models import *


# Create your views here.

def home_view(request):
    return render(request, 'home.html')


def ekskul_view(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    ekskul_data = DeskripsiEkskul.objects.filter(Q(nama_aplikasi__icontains=q) | Q(deskripsi__icontains=q))
    context = {
        'ekskul_data': ekskul_data
    }
    return render(request, 'ekskul.html', context)


def menu_view(request):
    home_data = DeskripsiHome.objects.all()

    if request.method == "GET":
        q = request.GET.get('q') if request.GET.get('q') is not None else ""
        home_data = DeskripsiHome.objects.filter(Q(nama_bidang__icontains=q) | Q(deskripsi__icontains=q))
    app_data = DeskripsiEkskul.objects.all()
    context = {
        'home_data': home_data,
        'app_data': app_data,
    }
    return render(request, 'menu.html', context)

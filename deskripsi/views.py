from django.shortcuts import render, redirect
from django.db.models import Q
from deskripsi.models import DeskripsiEkskul, DeskripsiHome
from userlog.models import UserLog
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def home_view(request):
    home_data = DeskripsiHome.objects.all()
    app_data = DeskripsiEkskul.objects.filter(status=True)
    logs = UserLog.objects.all().order_by('-created_at')[:10]

    if request.method == "POST":
        username = request.POST.get('username').rstrip()
        password = request.POST.get('pass').rstrip()


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login berhasil! Selamat datang..")
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="LOGIN",
                app="EKSKUL",
                message="Berhasil melakukan login ke aplikasi"
            )
            return redirect('app-index')
        else:
            messages.warning(request, "Username atau Password salah!")

    context = {
        'home_data': home_data,
        'app_data': app_data,
        'page': 'home',
        'logs': logs,
    }
    return render(request, 'home.html', context)


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
    app_data = DeskripsiEkskul.objects.filter(status=True)
    context = {
        'home_data': home_data,
        'app_data': app_data,
    }
    return render(request, 'menu.html', context)

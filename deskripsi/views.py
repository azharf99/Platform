from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from deskripsi.models import DeskripsiEkskul, DeskripsiHome
# from userlog.models import UserLog
from prestasi.models import Prestasi
# from django.contrib.auth import authenticate, login
# from django.contrib import messages

# Create your views here.

def home_view(request):
    # if request.user.is_authenticated:
    #     return redirect('dashboard')
    # home_data = DeskripsiHome.objects.all()
    # app_data = DeskripsiEkskul.objects.filter(status=True)
    # logs = UserLog.objects.all().order_by('-created_at')[:10]
    prestasi = Prestasi.objects.all().order_by('-created_at', '-tahun_lomba', 'peraih_prestasi')[:6]

    # if request.method == "POST":
    #     username = request.POST.get('username').rstrip()
    #     password = request.POST.get('pass').rstrip()


    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         login(request, user)
    #         messages.success(request, "Login berhasil! Selamat datang..")
    #         UserLog.objects.create(
    #             user=request.user.teacher,
    #             action_flag="LOGIN",
    #             app="EKSKUL",
    #             message="Berhasil melakukan login ke aplikasi"
    #         )
    #         return redirect('app-index')
    #     else:
    #         messages.warning(request, "Username atau Password salah!")

    context = {
        # 'home_data': home_data,
        # 'app_data': app_data,
        # 'page': 'home',
        # 'logs': logs,
        'prestasi': prestasi,
    }
    return render(request, 'new_home.html', context)
    # return render(request, 'new_home.html')


def ekskul_view(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    ekskul_data = DeskripsiEkskul.objects.filter(Q(nama_aplikasi__icontains=q) | Q(deskripsi__icontains=q))
    context = {
        'ekskul_data': ekskul_data
    }
    return render(request, 'new_ekskul.html', context)


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

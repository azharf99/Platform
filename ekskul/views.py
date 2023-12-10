import json

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib import sessions

from ekskul.models import Extracurricular, Student, StudentOrganization, Teacher, User
from ekskul.forms import InputAnggotaEkskulForm, PembinaEkskulForm, EkskulForm, CustomUserCreationForm, UsernameChangeForm, CustomPasswordChangeForm
from userlog.models import UserLog
from nilai.models import Penilaian
from dashboard.whatsapp import send_whatsapp_input_anggota, send_whatsapp_login
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView


# Create your views here.


class EkskulIndexView(ListView):
    model = Extracurricular
    template_name = 'new_extracurricular_list.html'
    paginate_by = 9

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
    template_name = 'new_data-detail.html'

    def get_context_data(self, **kwargs):
        context = super(EkskulDetailView, self).get_context_data(**kwargs)
        context['anggota'] = StudentOrganization.objects.filter(ekskul__slug=self.kwargs.get('slug')).order_by('siswa__kelas', 'siswa__nama_siswa')
        return context

class DataSantriView(ListView):
    model = StudentOrganization
    template_name = 'new_studentorganization_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        if query:
            # Use the 'q' parameter to filter the queryset
            queryset = StudentOrganization.objects.filter(siswa__nama_siswa__icontains=query)
        else:
            queryset = StudentOrganization.objects.all().order_by('siswa__kelas', 'siswa__nama_siswa')

        return queryset



class InputAnggotaView(LoginRequiredMixin, CreateView):
    model = StudentOrganization
    form_class = InputAnggotaEkskulForm
    template_name = 'new_input-anggota-ekskul.html'
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        data_ekskul = request.POST.get('ekskul_siswa')
        id_siswa = request.POST.get('siswa')
        try:
            self.object = StudentOrganization.objects.get(siswa_id=id_siswa, ekskul_id=data_ekskul)
            messages.error(request, "Santri sudah ada di dalam anggota ekskul. Silahkan pilih santri lain")
            return self.form_invalid(form)
        except:
            return self.form_valid(form)

    def form_valid(self, form):
        ekskul = get_object_or_404(Extracurricular, slug=self.kwargs.get('slug'))
        form.instance.ekskul = ekskul
        messages.success(self.request, "Input data berhasil! Silahkan cek pada daftar yang ada")
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="ADD",
            app="EKSKUL",
            message=f"Berhasil menambahkan anggota baru ekskul {ekskul}"
        )
        send_whatsapp_input_anggota(self.request.user.teacher.no_hp, ekskul.nama_ekskul, ekskul.tipe, f'data/{ekskul.slug}', 'input anggota')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ekskul'] = get_object_or_404(Extracurricular, slug=self.kwargs.get('slug'))
        return context

class DeleteAnggotaView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = StudentOrganization
    success_url = reverse_lazy('ekskul:data-index')
    template_name = 'new_delete-anggota.html'

    def get(self, request, *args, **kwargs):
        ekskul = get_object_or_404(Extracurricular, slug=self.kwargs.get('slug'))
        all = ekskul.pembina.all().values_list('user_id', flat=True)
        if not self.request.user.id in all and not self.request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
        return super().get(request, *args, **kwargs)
    def get_object(self, queryset=None):
        queryset = StudentOrganization.objects.get(siswa_id=self.kwargs.get('pk'), ekskul__slug=self.kwargs.get('slug'))
        return queryset

    def form_valid(self, form):
        ekskul = get_object_or_404(Extracurricular, slug=self.kwargs.get('slug'))
        all = ekskul.pembina.all().values_list('user_id', flat=True)
        if not self.request.user.id in all and not self.request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="DELETE",
            app="EKSKUL",
            message=f"Berhasil menghapus anggota baru ekskul {ekskul}"
        )
        send_whatsapp_input_anggota(self.request.user.teacher.no_hp, ekskul.nama_ekskul, ekskul.tipe, f'data/{ekskul.slug}', 'menghapus anggota')
        return super().form_valid(form)

class UpdateEskkulView(LoginRequiredMixin, UpdateView):
    model = Extracurricular
    template_name = 'new_edit-ekskul.html'
    form_class = EkskulForm

    def get(self, request, *args, **kwargs):
        ekskul = self.get_object()
        all = ekskul.pembina.all().values_list('user_id', flat=True)
        if not request.user.id in all and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('restricted'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        ekskul = self.get_object()
        UserLog.objects.create(
            user=self.request.user.teacher,
            action_flag="CHANGE",
            app="EKSKUL",
            message=f"Berhasil mengedit data ekskul {self.object}"
        )
        send_whatsapp_input_anggota(self.request.user.teacher.no_hp, ekskul.nama_ekskul, ekskul.tipe, f'data/{ekskul.slug}', 'mengedit data')
        return super().form_valid(form)

@login_required(login_url='/login/')
def input_pembina(request):
    form = PembinaEkskulForm().as_p()
    return render(request, 'input-anggota-ekskul.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get('username').rstrip()
        password = request.POST.get('password').rstrip()
        remember = request.POST.get('remember')
        
        if remember:
            request.session.set_expiry(1209600)
        else:
            request.session.set_expiry(0)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="LOGIN",
                app="EKSKUL",
                message="Berhasil melakukan login ke aplikasi"
            )
            send_whatsapp_login(request.user.teacher.no_hp, 'login', 'Selamat datang di Aplikasi PMBP')
            return redirect('dashboard')
        else:
            messages.warning(request, "Username atau Password salah!")
    context = {}
    return render(request, 'new_login.html', context)

@login_required(login_url='/login/')
def profil_view(request):
    teacher = get_object_or_404(Teacher, user_id = request.user.id)
    context = {
        'teacher': teacher,
        'name': "Overview",
    }
    return render(request, 'new_profil.html', context)

@login_required(login_url='/login/')
def edit_profil_view(request):
    try:
        teacher = Teacher.objects.get(user_id=request.user.id)
        form = PembinaEkskulForm(instance=teacher)
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
        context = {
            'form': form,
            'teacher': teacher,
            'name': "Edit Profile",
        }
    except:
        return redirect('login')
    return render(request, 'new_profil-edit.html', context)


def logout_view(request):
    UserLog.objects.create(
        user=request.user.teacher,
        action_flag="LOGOUT",
        app="EKSKUL",
        message="Berhasil logout dari aplikasi",
    )
    send_whatsapp_login(request.user.teacher.no_hp, 'logout', 'Kami sedih anda tinggalkan :(, namun tidak apa-apa, jangan lupa kembali ya')
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
            send_whatsapp_input_anggota(request.user.teacher.no_hp, 'anda', 'Profil', 'profil', 'mengubah')
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
            send_whatsapp_input_anggota(request.user.teacher.no_hp, 'anda', 'Password', 'profil', 'mengubah')
            return redirect('profil')

    context = {
        'forms': forms,
        'tipe' : 'change',
    }
    return render(request, 'register.html', context)

@csrf_exempt
def webhook_view(request):
    if request.method == 'POST':
        # Process the incoming webhook data here
        # For example, you can access the payload using `request.POST` or `request.body`

        # Replace this with your actual webhook processing logic
        dataku = json.loads(request.POST)
        message = dataku['message']
        phone = dataku['phone']
        url = f"https://jogja.wablas.com/api/send-message?phone={phone}&message={message}&token={settings.TOKEN}"
        requests.get(url)
        data = {
            'status': 'success',
            'message': 'Webhook received and processed successfully!',
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
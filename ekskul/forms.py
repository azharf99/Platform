from django import forms
from ekskul.models import StudentOrganization, Teacher, Extracurricular

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm


class InputAnggotaEkskulForm(forms.ModelForm):
    class Meta:
        model = StudentOrganization
        fields = '__all__'
        widgets  = {
            'nama_siswa': forms.Select(attrs={'id': 'input-anggota'})
        }


class PembinaEkskulForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['nama_lengkap', 'niy', 'gelar_depan', 'gelar_belakang', 'jabatan', 'jabatan_khusus', 'email', 'no_hp', 'foto']
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control'}),
            'niy': forms.NumberInput(attrs={'class': 'form-control'}),
            'gelar_depan': forms.TextInput(attrs={'class': 'form-control'}),
            'gelar_belakang': forms.TextInput(attrs={'class': 'form-control'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control'}),
            'jabatan_khusus': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'no_hp': forms.NumberInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
        }


class EkskulForm(forms.ModelForm):
    class Meta:
        model = Extracurricular
        fields = '__all__'
        exclude = ['slug']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'pembina': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'jadwal': forms.Select(attrs={'class': 'form-select'}),
            'waktu': forms.Select(attrs={'class': 'form-select'}),
            'jadwal_tambahan': forms.Select(attrs={'class': 'form-select'}),
            'waktu_tambahan': forms.Select(attrs={'class': 'form-select'}),
            'tipe': forms.Select(attrs={'class': 'form-select'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']

class UsernameChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']

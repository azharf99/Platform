from django import forms
from ekskul.models import StudentOrganization, Teacher, Extracurricular

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm


# class InputAnggotaEkskulForm(forms.Form):
#     class Meta:
#         model = StudentOrganization
#         fields = '__all__'
#         widgets  = {
#             'siswa': forms.Select(attrs={'id': 'input-anggota'})
#         }

class InputAnggotaEkskulForm(forms.ModelForm):
    class Meta:
        model = StudentOrganization
        fields = ['siswa']
        widgets  = {
            # 'ekskul': forms.Select(attrs={'class': 'form-control'}),
            'siswa': forms.Select(attrs={'id': 'input-anggota'})
        }



class PembinaEkskulForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['nama_pembina', 'niy', 'jenis_kelamin', 'jabatan', 'email', 'no_hp', 'alamat', 'foto']
        widgets = {
            'nama_pembina': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'niy': forms.NumberInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-select'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'no_hp': forms.NumberInput(attrs={'class': 'form-control'}),
            'alamat': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
        }


class EkskulForm(forms.ModelForm):
    class Meta:
        model = Extracurricular
        fields = '__all__'
        exclude = ['slug']
        widgets = {
            'nama_ekskul': forms.TextInput(attrs={'class': 'form-control'}),
            'pembina': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'jadwal': forms.Select(attrs={'class': 'form-select'}),
            'waktu': forms.Select(attrs={'class': 'form-select'}),
            'tipe': forms.Select(attrs={'class': 'form-select'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control'}),
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
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

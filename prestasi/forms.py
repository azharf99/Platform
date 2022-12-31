from django import forms
from prestasi.models import *


class PestasiInputForm(forms.ModelForm):
    class Meta:
        model = Prestasi
        fields = '__all__'
        widgets = {
            'kategori': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_lomba': forms.TextInput(attrs={'class': 'form-control'}),
            'tingkat_lomba': forms.TextInput(attrs={'class': 'form-control'}),
            'tahun_lomba': forms.DateInput(attrs={'class': 'form-control'}),
            'nama_lomba': forms.TextInput(attrs={'class': 'form-control'}),
            'Penyelenggara_lomba': forms.TextInput(attrs={'class': 'form-control'}),
            'peraih_prestasi': forms.TextInput(attrs={'class': 'form-control'}),
            'sekolah': forms.TextInput(attrs={'class': 'form-control'}),
            'bidang_lomba': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori_kemenangan': forms.TextInput(attrs={'class': 'form-control'}),
            'dokumentasi': forms.Select(attrs={'class': 'form-select'}),
        }
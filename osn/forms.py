from django import forms
from osn.models import BidangOSN, SiswaOSN, LaporanOSN

class FormInputBidang(forms.ModelForm):
    class Meta:
        model = BidangOSN
        fields = '__all__'
        widgets = {
            'nama_bidang': forms.TextInput(attrs={'class': 'form-control'}),
            'pembimbing': forms.Select(attrs={'class': 'form-select'}),
            'jadwal_bimbingan': forms.Textarea(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FormInputSiswa(forms.ModelForm):
    class Meta:
        model = SiswaOSN
        fields = '__all__'
        widgets = {
            'bidang_osn': forms.Select(attrs={'class': 'form-select'}),
            'nama_siswa': forms.Select(attrs={'class': 'form-select'}),
        }


class FormInputLaporanOSN(forms.ModelForm):
    class Meta:
        model = LaporanOSN
        fields = '__all__'
        widgets = {
            'pembimbing_osn': forms.Select(attrs={'class': 'form-select'}),
            'bidang_osn': forms.Select(attrs={'class': 'form-select'}),
            'tanggal_pembinaan': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'kehadiran_santri': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'foto_bimbingan': forms.FileInput(attrs={'class': 'form-control'}),
            'materi_pembinaan': forms.Textarea(attrs={'class': 'form-control'}),
        }


class FormEditLaporanOSN(forms.ModelForm):
    class Meta:
        model = LaporanOSN
        fields = '__all__'
        widgets = {
            'pembimbing_osn': forms.Select(attrs={'class': 'form-select'}),
            'bidang_osn': forms.Select(attrs={'class': 'form-select'}),
            'tanggal_pembinaan': forms.DateInput(attrs={'class': 'form-control'}),
            'kehadiran_santri': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'materi_pembinaan': forms.Textarea(attrs={'class': 'form-control'}),
        }
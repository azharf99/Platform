from django import forms
from inventaris.models import *

class InventarisInputForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        widgets = {
            'nama_barang': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah': forms.NumberInput(attrs={'class': 'form-control'}),
            'pemilik': forms.Select(attrs={'class': 'form-select'}),
            'hibah': forms.Select(attrs={'class': 'form-select'}),
            'pemberi_hibah': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_hibah': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_dibeli': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'anggaran_dana': forms.NumberInput(attrs={'class': 'form-control'}),
            'nama_toko': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat_toko': forms.Textarea(attrs={'class': 'form-control'}),
        }
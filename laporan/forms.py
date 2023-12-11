from django import forms
from laporan.models import Report

class FormLaporanKehadiran(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['nama_ekskul', 'pembina_ekskul', 'tanggal_pembinaan', 'kehadiran_santri', 'foto', 'catatan_pembinaan'] 
        widgets = {
            'nama_ekskul': forms.Select(attrs={'class': 'form-select'}),
            'pembina_ekskul': forms.Select(attrs={'class': 'form-select'}),
            'tanggal_pembinaan': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'catatan_pembinaan': forms.TextInput(attrs={'class': 'form-control'}),
            'kehadiran_santri': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

# class FormUploadLaporanKehadiran(forms.ModelForm):
#     class Meta:
#         model = UploadImage
#         fields = ['foto_absensi']
#         widgets = {
#             'foto_absensi': forms.FileInput(attrs={'class': 'form-control', 'required': True}),
#         }
#
# class FormEditUploadLaporanKehadiran(forms.ModelForm):
#     class Meta:
#         model = UploadImage
#         fields = ['foto_absensi']
#         widgets = {
#             'laporan': forms.Select(attrs={'class': 'form-select', 'disabled': True}),
#         }
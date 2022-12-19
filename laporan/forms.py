from django import forms
from laporan.models import Report, UploadImage

class LaporanKehadiran(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'

class UploadLaporanKehadiran(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = '__all__'
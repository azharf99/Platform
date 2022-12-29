from django import forms
from nilai.models import Penilaian

class NilaiForm(forms.ModelForm):
    class Meta:
        model = Penilaian
        fields = '__all__'
        widgets = {
            'nilai': forms.Select(attrs={'class':'form-select'})
        }


class NilaiEditForm(forms.ModelForm):
    class Meta:
        model = Penilaian
        fields = ['nilai']
        widgets = {
            'nilai': forms.Select(attrs={'class':'form-select'})
        }
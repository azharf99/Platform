from django import forms
from ekskul.models import *


class InputAnggotaEkskulForm(forms.ModelForm):
    class Meta:
        model = StudentOrganization
        fields = '__all__'


class PembinaEkskulForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'


class EkskulForm(forms.ModelForm):
    class Meta:
        model = Extracurricular
        fields = '__all__'
        exclude = ['slug']

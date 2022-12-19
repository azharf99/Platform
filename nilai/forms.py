from django import forms
from nilai.models import Penilaian

class NilaiForm(forms.ModelForm):
    class Meta:
        model = Penilaian
        fields = '__all__'
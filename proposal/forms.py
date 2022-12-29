from django import forms
from proposal.models import *


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = '__all__'
        widgets = {
            'nama_event': forms.TextInput(attrs={'class': 'form-control'}),
            'pembuat_event': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_pendaftaran': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_penyisihan_1': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_penyisihan_2': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_penyisihan_3': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_semifinal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pengumuman_pemenang': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pelaksanaan': forms.Select(attrs={'class': 'form-select'}),
            'tingkat_event': forms.Select(attrs={'class': 'form-select'}),
            'berjenjang': forms.Select(attrs={'class': 'form-select'}),
            'lokasi_event': forms.TextInput(attrs={'class': 'form-control'}),
            'kota': forms.TextInput(attrs={'class': 'form-control'}),
            'provinsi': forms.TextInput(attrs={'class': 'form-control'}),
            'penanggungjawab': forms.Select(attrs={'class': 'form-select'}),
            'ekskul': forms.Select(attrs={'class': 'form-select'}),
            'santri': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'anggaran_biaya': forms.NumberInput(attrs={'class': 'form-control'}),
            'upload_brosur': forms.FileInput(attrs={'class': 'form-control'}),
            'upload_undangan': forms.FileInput(attrs={'class': 'form-control'}),
            'upload_file': forms.FileInput(attrs={'class': 'form-control'}),
            'Catatan': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ProposalEditForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = '__all__'
        widgets = {
            'nama_event': forms.TextInput(attrs={'class': 'form-control'}),
            'pembuat_event': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_pendaftaran': forms.DateInput(attrs={'class': 'form-control'}),
            'tanggal_penyisihan_1': forms.DateInput(attrs={'class': 'form-control'}),
            'tanggal_penyisihan_2': forms.DateInput(attrs={'class': 'form-control'}),
            'tanggal_penyisihan_3': forms.DateInput(attrs={'class': 'form-control'}),
            'tanggal_semifinal': forms.DateInput(attrs={'class': 'form-control'}),
            'tanggal_final': forms.DateInput(attrs={'class': 'form-control'}),
            'pengumuman_pemenang': forms.DateInput(attrs={'class': 'form-control'}),
            'pelaksanaan': forms.Select(attrs={'class': 'form-select'}),
            'tingkat_event': forms.Select(attrs={'class': 'form-select'}),
            'berjenjang': forms.Select(attrs={'class': 'form-select'}),
            'lokasi_event': forms.TextInput(attrs={'class': 'form-control'}),
            'kota': forms.TextInput(attrs={'class': 'form-control'}),
            'provinsi': forms.TextInput(attrs={'class': 'form-control'}),
            'penanggungjawab': forms.Select(attrs={'class': 'form-select'}),
            'ekskul': forms.Select(attrs={'class': 'form-select'}),
            'santri': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'anggaran_biaya': forms.NumberInput(attrs={'class': 'form-control'}),
            'Catatan': forms.Textarea(attrs={'class': 'form-control'}),
        }


class StatusProposalForm(forms.ModelForm):
    class Meta:
        model = ProposalStatus
        fields = ['proposal', 'is_wakasek', 'alasan_wakasek', 'foto_alasan']
        widgets = {
            'proposal': forms.Select(attrs={'class': 'form-control'}),
            'is_wakasek': forms.Select(attrs={'class': 'form-select'}),
            'alasan_wakasek': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_alasan': forms.FileInput(attrs={'class': 'form-control'}),
        }


class StatusProposalKepsekForm(forms.ModelForm):
    class Meta:
        model = ProposalStatusKepsek
        fields = ['is_kepsek', 'alasan_kepsek', 'foto_alasan']
        widgets = {
            'is_kepsek': forms.Select(attrs={'class': 'form-select'}),
            'alasan_kepsek': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_alasan': forms.FileInput(attrs={'class': 'form-control'}),
        }


class StatusProposalBendaharaForm(forms.ModelForm):
    class Meta:
        model = ProposalStatusBendahara
        fields = ['is_bendahara', 'alasan_bendahara', 'foto_alasan']
        widgets = {
            'proposal': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'status_kepsek': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'is_bendahara': forms.Select(attrs={'class': 'form-select'}),
            'alasan_bendahara': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_alasan': forms.FileInput(attrs={'class': 'form-control'}),
        }

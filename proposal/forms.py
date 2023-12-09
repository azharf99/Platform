from django import forms
from proposal.models import Proposal, ProposalStatus, ProposalStatusKepsek, ProposalStatusBendahara, ProposalInventaris, ProposalInventarisStatus, ProposalInventarisStatusKepsek, ProposalInventarisStatusBendahara


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = '__all__'
        widgets = {
            'nama_event': forms.TextInput(attrs={'class': 'form-control'}),
            'pembuat_event': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_pendaftaran': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_pelaksanaan': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pelaksanaan': forms.Select(attrs={'class': 'form-select'}),
            'tingkat_event': forms.Select(attrs={'class': 'form-select'}),
            'lokasi_event': forms.TextInput(attrs={'class': 'form-control'}),
            'penanggungjawab': forms.Select(attrs={'class': 'form-select'}),
            'nomor_rekening': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_bank': forms.TextInput(attrs={'class': 'form-control'}),
            'ekskul': forms.Select(attrs={'class': 'form-select'}),
            'santri': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'anggaran_biaya': forms.NumberInput(attrs={'class': 'form-control'}),
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
            'tanggal_pendaftaran': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_pelaksanaan': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pelaksanaan': forms.Select(attrs={'class': 'form-control'}),
            'tingkat_event': forms.Select(attrs={'class': 'form-select'}),
            'lokasi_event': forms.TextInput(attrs={'class': 'form-control'}),
            'penanggungjawab': forms.Select(attrs={'class': 'form-select'}),
            'nomor_rekening': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_bank': forms.TextInput(attrs={'class': 'form-control'}),
            'ekskul': forms.Select(attrs={'class': 'form-select'}),
            'santri': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'anggaran_biaya': forms.NumberInput(attrs={'class': 'form-control'}),
            'Catatan': forms.Textarea(attrs={'class': 'form-control'}),
        }


class StatusProposalForm(forms.ModelForm):
    class Meta:
        model = ProposalStatus
        fields = ['proposal', 'is_wakasek', 'alasan_wakasek']
        widgets = {
            'proposal': forms.Select(attrs={'class': 'form-control'}),
            'is_wakasek': forms.Select(attrs={'class': 'form-select'}),
            'alasan_wakasek': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StatusProposalKepsekForm(forms.ModelForm):
    class Meta:
        model = ProposalStatusKepsek
        fields = ['is_kepsek', 'alasan_kepsek']
        widgets = {
            'is_kepsek': forms.Select(attrs={'class': 'form-select'}),
            'alasan_kepsek': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StatusProposalBendaharaForm(forms.ModelForm):
    class Meta:
        model = ProposalStatusBendahara
        fields = ['is_bendahara', 'alasan_bendahara', 'bukti_transfer', 'catatan_bendahara']
        widgets = {
            'proposal': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'status_kepsek': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'is_bendahara': forms.Select(attrs={'class': 'form-select'}),
            'alasan_bendahara': forms.TextInput(attrs={'class': 'form-control'}),
            'bukti_transfer': forms.FileInput(attrs={'class': 'form-control'}),
            'catatan_bendahara': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ProposalInventarisForm(forms.ModelForm):
    class Meta:
        model = ProposalInventaris
        fields = '__all__'
        widgets = {
            'judul_proposal': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_pembelian': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nama_toko': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat_toko': forms.TextInput(attrs={'class': 'form-control'}),
            'penanggungjawab': forms.Select(attrs={'class': 'form-select'}),
            'nomor_rekening': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_bank': forms.TextInput(attrs={'class': 'form-control'}),
            'ekskul': forms.Select(attrs={'class': 'form-select'}),
            'santri': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'anggaran_biaya': forms.NumberInput(attrs={'class': 'form-control'}),
            'upload_file': forms.FileInput(attrs={'class': 'form-control'}),
            'Catatan': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProposalInventarisEditForm(forms.ModelForm):
    class Meta:
        model = ProposalInventaris
        fields = '__all__'
        widgets = {
            'judul_proposal': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_pembelian': forms.DateInput(attrs={'class': 'form-control'}),
            'nama_toko': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat_toko': forms.TextInput(attrs={'class': 'form-control'}),
            'penanggungjawab': forms.Select(attrs={'class': 'form-select'}),
            'nomor_rekening': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_bank': forms.TextInput(attrs={'class': 'form-control'}),
            'ekskul': forms.Select(attrs={'class': 'form-select'}),
            'santri': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'anggaran_biaya': forms.NumberInput(attrs={'class': 'form-control'}),
            'upload_file': forms.FileInput(attrs={'class': 'form-control'}),
            'Catatan': forms.Textarea(attrs={'class': 'form-control'}),
        }

class StatusProposalInventarisForm(forms.ModelForm):
    class Meta:
        model = ProposalInventarisStatus
        fields = ['proposal', 'is_wakasek', 'alasan_wakasek']
        widgets = {
            'proposal': forms.Select(attrs={'class': 'form-control'}),
            'is_wakasek': forms.Select(attrs={'class': 'form-select'}),
            'alasan_wakasek': forms.TextInput(attrs={'class': 'form-control'})
        }


class StatusProposalInventarisKepsekForm(forms.ModelForm):
    class Meta:
        model = ProposalInventarisStatusKepsek
        fields = ['is_kepsek', 'alasan_kepsek']
        widgets = {
            'is_kepsek': forms.Select(attrs={'class': 'form-select'}),
            'alasan_kepsek': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StatusProposalInventarisBendaharaForm(forms.ModelForm):
    class Meta:
        model = ProposalInventarisStatusBendahara
        fields = ['is_bendahara', 'alasan_bendahara', 'bukti_transfer', 'catatan_bendahara']
        widgets = {
            'proposal': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'status_kepsek': forms.Select(attrs={'class': 'form-control', 'disabled': True}),
            'is_bendahara': forms.Select(attrs={'class': 'form-select'}),
            'alasan_bendahara': forms.TextInput(attrs={'class': 'form-control'}),
            'bukti_transfer': forms.FileInput(attrs={'class': 'form-control'}),
            'catatan_bendahara': forms.Textarea(attrs={'class': 'form-control'}),
        }

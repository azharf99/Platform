from django import forms
from inventaris.models import Invoice, Inventory, InventoryStatus


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


class InventarisEditForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        widgets = {
            'nama_barang': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah': forms.NumberInput(attrs={'class': 'form-control'}),
            'pemilik': forms.Select(attrs={'class': 'form-select'}),
            'hibah': forms.Select(attrs={'class': 'form-select'}),
            'pemberi_hibah': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_hibah': forms.DateInput(attrs={'class': 'form-control'}),
            'tanggal_dibeli': forms.DateInput(attrs={'class': 'form-control'}),
            'anggaran_dana': forms.NumberInput(attrs={'class': 'form-control'}),
            'nama_toko': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat_toko': forms.Textarea(attrs={'class': 'form-control'}),
        }


class InventarisStatusInputForm(forms.ModelForm):
    class Meta:
        model = InventoryStatus
        fields = '__all__'
        widgets = {
            'barang': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'peminjam': forms.TextInput(attrs={'class': 'form-control'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control'}),
        }


class InventarisStatusEditForm(forms.ModelForm):
    class Meta:
        model = InventoryStatus
        fields = '__all__'
        widgets = {
            'barang': forms.Select(attrs={'class': 'form-select', 'disabled': True}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'peminjam': forms.TextInput(attrs={'class': 'form-control'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control'}),
        }

class InventarisInvoiceInputForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'barang': forms.Select(attrs={'class': 'form-select'}),
            'foto_nota': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels ={
            'foto_nota': "Nota Barang"
        }

class InventarisInvoiceEditForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'barang': forms.Select(attrs={'class': 'form-select', 'disabled': True}),
        }
        labels = {
            'foto_nota': "Nota Barang"
        }
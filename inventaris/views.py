from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from inventaris.forms import InventarisInputForm, InventarisEditForm, InventarisStatusInputForm, InventarisStatusEditForm, InventarisInvoiceInputForm, InventarisInvoiceEditForm
from inventaris.models import Inventory, InventoryStatus, Invoice
from userlog.models import UserLog


# Create your views here.


def index(request):
    inventaris = Inventory.objects.all()
    context = {
        'inventaris': inventaris,
    }
    return render(request, 'inventaris.html', context)


def inventaris_detail(request, pk):
    data = get_object_or_404(Inventory, id=pk)
    context = {
        'data': data,
    }
    return render(request, 'inventaris-detail.html', context)


@login_required(login_url='/login/')
def inventaris_input(request):
    if not request.user.is_superuser:
        return redirect('restricted')
    if request.method == "POST":
        nama_barang = request.POST.get('nama_barang')
        forms = InventarisInputForm(request.POST)
        if forms.is_valid():
            forms.save()
            data = Inventory.objects.get(nama_barang=nama_barang)
            InventoryStatus.objects.create(
                barang=data,
                status="Tersedia",
                peminjam="",
                keterangan=""
            )
            Invoice.objects.create(
                barang=data
            )
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="ADD",
                app="INVENTARIS",
                message="Berhasil menambahkan data inventaris {}".format(nama_barang)
            )
            return redirect('inventaris:inventaris-index')
    else:
        forms = InventarisInputForm()

    context = {
        'forms': forms,
    }
    return render(request, 'inventaris-input.html', context)


@login_required(login_url='/login/')
def inventaris_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('restricted')
    inventory = get_object_or_404(Inventory, id=pk)
    if request.method == "POST":
        forms = InventarisEditForm(request.POST, instance=inventory)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="INVENTARIS",
                message="Berhasil mengubah data inventaris {}".format(inventory.nama_barang)
            )
            return redirect('inventaris:inventaris-index')
    else:
        forms = InventarisEditForm(instance=inventory)

    context = {
        'forms': forms,
    }
    return render(request, 'inventaris-input.html', context)


@login_required(login_url='/login/')
def inventaris_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('restricted')
    inventory = get_object_or_404(Inventory, id=pk)
    if request.method == "POST":
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DELETE",
            app="INVENTARIS",
            message="Berhasil menghapus data inventaris {}".format(inventory.nama_barang)
        )
        inventory.delete()
        return redirect('inventaris:inventaris-index')

    context = {
        'inventory': inventory,
    }
    return render(request, 'inventaris-delete.html', context)


def inventaris_status_detail(request, pk):
    data = get_object_or_404(InventoryStatus, barang_id=pk)
    context = {
        'data': data,
    }
    return render(request, 'inventaris-status-detail.html', context)


@login_required(login_url='/login/')
def inventaris_status_input(request):
    if not request.user.is_superuser:
        return redirect('restricted')
    if request.method == "POST":
        nama_barang = request.POST.get('nama_barang')
        forms = InventarisStatusInputForm(request.POST)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="ADD",
                app="INVENTARIS_STATUS",
                message="Berhasil menambahkan data status inventaris {}".format(nama_barang)
            )
            return redirect('inventaris:inventaris-index')
    else:
        forms = InventarisStatusInputForm()

    context = {
        'forms': forms,
    }
    return render(request, 'inventaris-status-input.html', context)


@login_required(login_url='/login/')
def inventaris_status_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('restricted')
    inventory = get_object_or_404(InventoryStatus, id=pk)
    if request.method == "POST":
        forms = InventarisStatusEditForm(request.POST, instance=inventory)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="INVENTARIS_STATUS",
                message="Berhasil mengubah data status inventaris {}".format(inventory.barang)
            )
            return redirect('inventaris:inventaris-index')
    else:
        forms = InventarisStatusEditForm(instance=inventory)

    context = {
        'forms': forms,
    }
    return render(request, 'inventaris-status-input.html', context)


@login_required(login_url='/login/')
def inventaris_status_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('restricted')
    inventory_status = get_object_or_404(InventoryStatus, id=pk)
    if request.method == "POST":
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DELETE",
            app="INVENTARIS",
            message="Berhasil menghapus data status inventaris {}".format(inventory_status.barang)
        )
        inventory_status.delete()
        return redirect('inventaris:inventaris-index')

    context = {
        'inventory_status': inventory_status,
    }
    return render(request, 'inventaris-status-delete.html', context)


def inventaris_invoice_detail(request, pk):
    data = get_object_or_404(Invoice, barang_id=pk)
    context = {
        'data': data,
    }
    return render(request, 'inventaris-invoice-detail.html', context)


@login_required(login_url='/login/')
def inventaris_invoice_input(request):
    if not request.user.is_superuser:
        return redirect('restricted')
    if request.method == "POST":
        nama_barang = request.POST.get('nama_barang')
        forms = InventarisInvoiceInputForm(request.POST)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="ADD",
                app="INVENTARIS_STATUS",
                message="Berhasil menambahkan data status inventaris {}".format(nama_barang)
            )
            return redirect('inventaris:inventaris-index')
    else:
        forms = InventarisInvoiceInputForm()

    context = {
        'forms': forms,
    }
    return render(request, 'inventaris-invoice-input.html', context)


@login_required(login_url='/login/')
def inventaris_invoice_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('restricted')
    inventory = get_object_or_404(Invoice, id=pk)
    if request.method == "POST":
        forms = InventarisInvoiceEditForm(request.POST, request.FILES, instance=inventory)
        if forms.is_valid():
            forms.save()
            UserLog.objects.create(
                user=request.user.teacher,
                action_flag="CHANGE",
                app="INVENTARIS_STATUS",
                message="Berhasil mengubah data status inventaris {}".format(inventory.barang)
            )
            return redirect('inventaris:inventaris-index')
    else:
        forms = InventarisInvoiceEditForm(instance=inventory)

    context = {
        'forms': forms,
    }
    return render(request, 'inventaris-invoice-input.html', context)


@login_required(login_url='/login/')
def inventaris_invoice_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('restricted')
    invoice = get_object_or_404(Invoice, id=pk)
    if request.method == "POST":
        UserLog.objects.create(
            user=request.user.teacher,
            action_flag="DELETE",
            app="INVENTARIS",
            message="Berhasil menghapus data status inventaris {}".format(invoice.barang)
        )
        invoice.delete()
        return redirect('inventaris:inventaris-index')

    context = {
        'invoice': invoice,
    }
    return render(request, 'inventaris-invoice-delete.html', context)
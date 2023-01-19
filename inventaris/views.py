from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from inventaris.forms import *
from inventaris.models import *
from userlog.models import UserLog


# Create your views here.


def index(request):
    inventaris = Inventory.objects.all()
    context = {
        'inventaris': inventaris,
    }
    return render(request, 'inventaris.html', context)


@login_required(login_url='/login/')
def inventaris_input(request):
    if request.method == "POST":
        nama_barang = request.POST.get('nama_barang')
        forms = InventarisInputForm(request.POST)
        if forms.is_valid():
            forms.save()
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


def inventaris_detail(request, pk):
    data = get_object_or_404(Inventory, id=pk)
    context = {
        'data': data,
    }
    return render(request, 'inventaris-detail.html', context)

@login_required(login_url='/login/')
def inventaris_edit(request, pk):
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
    inventory = get_object_or_404(Inventory, id=pk)
    if request.method == "POST":
        inventory.delete()
        UserLog.objects.create(
                user=request.user.teacher,
                action_flag="DELETE",
                app="INVENTARIS",
                message="Berhasil menghapus data inventaris {}".format(inventory.nama_barang)
        )
        return redirect('inventaris:inventaris-index')

    context = {
        'inventory': inventory,
    }
    return render(request, 'inventaris-delete.html', context)

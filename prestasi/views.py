from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from prestasi.forms import PrestasiInputForm, PrestasiEditForm, DokumentasiPrestasiEditForm, DokumentasiPrestasiInputForm
from prestasi.models import Prestasi, DokumentasiPrestasi
from django.contrib import messages


# Create your views here.

def index(request):
    prestasi = Prestasi.objects.all()
    context = {
        'prestasi': prestasi
    }
    return render(request, 'prestasi.html', context)


def prestasi_detail(request, pk):
    data = get_object_or_404(Prestasi, id=pk)
    context = {
        'data': data,
    }
    return render(request, 'prestasi-detail.html', context)


@login_required(login_url="/login/")
def prestasi_input(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        forms = PrestasiInputForm(request.POST, request.FILES)
        if forms.is_valid():
            f = forms.save()
            DokumentasiPrestasi.objects.create(
                prestasi=f,
            )
            return redirect('prestasi:prestasi-index')
        else:
            forms = PrestasiInputForm(request.POST, request.FILES)
            messages.error(request, "Yang kamu isi ada yang salah dalam isiannya. Tolong diperiksa lagi.")
    else:
        forms = PrestasiInputForm()

    context = {
        'forms': forms,
    }
    return render(request, 'prestasi-input.html', context)


@login_required(login_url="/login/")
def prestasi_edit(request, pk):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    data = get_object_or_404(Prestasi, id=pk)
    if request.method == 'POST':
        forms = PrestasiEditForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            return redirect('prestasi:prestasi-index')
        else:
            forms = PrestasiEditForm(request.POST)
            messages.error(request, "Yang kamu isi ada yang salah dalam isiannya. Tolong diperiksa lagi.")
    else:
        forms = PrestasiEditForm(instance=data)

    context = {
        'forms': forms,
    }
    return render(request, 'prestasi-input.html', context)


@login_required(login_url="/login/")
def prestasi_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    data = get_object_or_404(Prestasi, id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('prestasi:prestasi-index')

    context = {
        'data': data,
    }
    return render(request, 'prestasi-delete.html', context)


def dokumentasi_prestasi_detail(request, pk):
    data = get_object_or_404(DokumentasiPrestasi, prestasi_id=pk)
    context = {
        'data': data,
    }
    return render(request, 'prestasi-foto-detail.html', context)

@login_required(login_url="/login/")
def dokumentasi_prestasi_input(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    if request.method == 'POST':
        forms = DokumentasiPrestasiInputForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('prestasi:prestasi-index')
        else:
            forms = DokumentasiPrestasiInputForm(request.POST, request.FILES)
            messages.error(request, "Yang kamu isi ada yang salah dalam isiannya. Tolong diperiksa lagi.")
    else:
        forms = DokumentasiPrestasiInputForm()

    context = {
        'forms': forms,
    }
    return render(request, 'prestasi-foto-input.html', context)


@login_required(login_url="/login/")
def dokumentasi_prestasi_edit(request, pk):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    data = get_object_or_404(DokumentasiPrestasi, id=pk)
    if request.method == 'POST':
        forms = DokumentasiPrestasiEditForm(request.POST, request.FILES, instance=data)
        if forms.is_valid():
            forms.save()
            return redirect('prestasi:prestasi-index')
        else:
            forms = DokumentasiPrestasiEditForm(request.POST, request.FILES)
            messages.error(request, "Yang kamu isi ada yang salah dalam isiannya. Tolong diperiksa lagi.")
    else:
        forms = DokumentasiPrestasiEditForm(instance=data)

    context = {
        'forms': forms,
    }
    return render(request, 'prestasi-foto-input.html', context)


@login_required(login_url="/login/")
def dokumentasi_prestasi_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('restricted'))
    data = get_object_or_404(DokumentasiPrestasi, id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('prestasi:prestasi-index')

    context = {
        'data': data,
    }
    return render(request, 'prestasi-foto-delete.html', context)

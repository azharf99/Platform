from django.shortcuts import render, redirect
from inventaris.forms import *
from inventaris.models import *

# Create your views here.


def index(request):
    inventaris = Inventory.objects.all()
    context = {
        'inventaris': inventaris,
    }
    return render(request, 'inventaris.html', context)


def inventaris_input(request):
    if request.method == "POST":
        forms = InventarisInputForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('inventaris:inventaris-index')
    else:
        forms = InventarisInputForm()

    context = {
        'forms': forms,
    }
    return render(request, 'inventaris-input.html', context)
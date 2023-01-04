from django.shortcuts import render, redirect
from prestasi.forms import *
from prestasi.models import *
from django.contrib import messages

# Create your views here.

def index(request):
    prestasi = Prestasi.objects.all()
    context = {
        'prestasi': prestasi
    }
    return render(request, 'prestasi.html', context)

def prestasi_input(request):
    if request.method == 'POST':
        forms = PestasiInputForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('prestasi-page')
        else:
            forms = PestasiInputForm(request.POST)
            messages.error(request, "Yang kamu isi ada yang salah dalam isiannya. Tolong diperiksa lagi.")
    else:
        forms = PestasiInputForm()

    context = {
        'forms': forms,
    }
    return render(request, 'prestasi-input.html', context)

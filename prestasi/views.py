from django.shortcuts import render
from prestasi.models import *

# Create your views here.

def index(request):
    prestasi = Prestasi.objects.all()
    context = {
        'prestasi': prestasi
    }
    return render(request, 'prestasi.html', context)

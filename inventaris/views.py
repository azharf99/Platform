from django.shortcuts import render
from inventaris.models import *

# Create your views here.


def index(request):
    inventaris = Inventory.objects.all()
    context = {
        'inventaris': inventaris,
    }
    return render(request, 'inventaris.html', context)
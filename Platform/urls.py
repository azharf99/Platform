"""Platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def home_ekskul(request):
    return render(request, 'ekskul.html')
def prestasi(request):
    return render(request, 'prestasi.html')
def struktur(request):
    return render(request, 'struktur.html')
def unduh(request):
    return render(request, 'unduh.html')

def not_available(request):
    return render(request, 'notavailable.html')

urlpatterns = [
    path('', home, name='app-index'),
    path('admin/', admin.site.urls),
    path('ekskul/', home_ekskul, name='ekskul-page'),
    path('ekskul/proposal/', include('proposal.urls')),
    path('ekskul/laporan/', include('laporan.urls')),
    path('ekskul/nilai/', include('nilai.urls')),
    path('ekskul/data/', include('ekskul.urls')),
    path('ekskul/inventaris/', include('inventaris.urls')),
    path('ekskul/timeline/', include('timeline.urls')),
    path('ekskul/prestasi/', prestasi, name='prestasi-page'),
    path('ekskul/struktur/', struktur, name='struktur-page'),
    path('ekskul/unduh/', unduh, name='unduh-page'),
    path('notavailable/', not_available, name='not-available'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

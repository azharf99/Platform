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

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('ekskul/', home_ekskul),
    path('ekskul/proposal/', include('proposal.urls')),
    path('ekskul/laporan/', include('laporan.urls')),
    path('ekskul/nilai/', include('nilai.urls')),
    path('ekskul/data/', include('ekskul.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

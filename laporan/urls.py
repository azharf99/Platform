from django.urls import path
from laporan import views

urlpatterns = [
    path('', views.index, name='laporan-index')
]
from django.urls import path
from laporan import views

app_name = 'laporan'
urlpatterns = [
    path('', views.index, name='laporan-index'),
    path('<slug:slug>', views.laporan_detail, name='laporan-detail'),
    path('<slug:slug>/input', views.laporan_input, name='laporan-input'),
    path('<slug:slug>/upload', views.laporan_upload, name='laporan-upload'),
]
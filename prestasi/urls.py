from django.urls import path
from prestasi import views

app_name = 'prestasi'
urlpatterns = [
    path('', views.index, name='prestasi-index'),
    path('input', views.prestasi_input, name='prestasi-input'),
    path('detail/<int:pk>', views.prestasi_detail, name='prestasi-detail'),
    path('edit/<int:pk>', views.prestasi_edit, name='prestasi-edit'),
    path('delete/<int:pk>', views.prestasi_delete, name='prestasi-delete'),
    path('foto/input', views.dokumentasi_prestasi_input, name='prestasi-foto-input'),
    path('foto/detail/<int:pk>', views.dokumentasi_prestasi_detail, name='prestasi-foto-detail'),
    path('foto/edit/<int:pk>', views.dokumentasi_prestasi_edit, name='prestasi-foto-edit'),
    path('foto/delete/<int:pk>', views.dokumentasi_prestasi_delete, name='prestasi-foto-delete'),
]
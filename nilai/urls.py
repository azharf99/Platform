from django.urls import path
from nilai import views

app_name = 'nilai'
urlpatterns = [
    path('', views.index, name='nilai-index'),
    path('kelas', views.nilai_kelas_view, name='nilai-per-kelas'),
    path('<slug:slug>', views.nilai_detail, name='nilai-detail'),
    path('<slug:slug>/input', views.nilai_input, name='nilai-input'),
    path('<slug:slug>/edit/<int:pk>', views.nilai_edit, name='nilai-edit'),
    path('<slug:slug>/delete/<int:pk>', views.nilai_delete, name='nilai-delete'),
]
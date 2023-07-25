from django.urls import path
from nilai import views

app_name = 'nilai'
urlpatterns = [
    path('', views.NilaiIndexView.as_view(), name='nilai-index'),
    path('kelas', views.nilai_kelas_view, name='nilai-per-kelas'),
    path('download', views.print_to_excel, name='print-to-excel'),
    path('<slug:slug>', views.nilai_detail, name='nilai-detail'),
    path('<slug:slug>/input', views.nilai_input, name='nilai-input'),
    path('<slug:slug>/edit/<int:pk>', views.nilai_edit, name='nilai-edit'),
    path('<slug:slug>/delete/<int:pk>', views.nilai_delete, name='nilai-delete'),
]
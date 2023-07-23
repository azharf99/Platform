from django.urls import path
from laporan import views

app_name = 'laporan'
urlpatterns = [
    path('', views.index, name='laporan-index'),
    path('<slug:slug>', views.laporan_ekskul, name='laporan-ekskul'),
    path('<slug:slug>/print', views.print_to_pdf, name='laporan-print'),
    path('<slug:slug>/print2', views.laporan_ekskul_print_versi2, name='laporan-print-v2'),
    path('<slug:slug>/input', views.laporan_input, name='laporan-input'),
    path('<slug:slug>/detail/<int:pk>', views.laporan_detail, name='laporan-detail'),
    path('<slug:slug>/edit/<int:pk>', views.laporan_edit, name='laporan-edit'),
    path('<slug:slug>/delete/<int:pk>', views.laporan_delete, name='laporan-delete'),
    path('<slug:slug>/upload', views.laporan_upload, name='laporan-upload'),
    path('<slug:slug>/upload/edit/<int:pk>', views.laporan_upload_edit, name='laporan-upload-edit'),
    path('<slug:slug>/upload/delete/<int:pk>', views.laporan_upload_delete, name='laporan-upload-delete'),
]
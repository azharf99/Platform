from django.urls import path
from laporan import views

app_name = 'laporan'
urlpatterns = [
    path('', views.LaporanIndexView.as_view(), name='laporan-index'),
    path('<slug:slug>', views.LaporanEkskulView.as_view(), name='laporan-ekskul'),
    path('<slug:slug>/print', views.PrintToPrintView.as_view(), name='laporan-print'),
    path('<slug:slug>/pdf', views.PrintToPDFView.as_view(), name='laporan-pdf'),
    path('<slug:slug>/print2', views.laporan_ekskul_print_versi2, name='laporan-print-v2'),
    path('<slug:slug>/input', views.laporan_input, name='laporan-input'),
    path('<slug:slug>/detail/<int:pk>', views.LaporanDetailView.as_view(), name='laporan-detail'),
    path('<slug:slug>/edit/<int:pk>', views.laporan_edit, name='laporan-edit'),
    path('<slug:slug>/delete/<int:pk>', views.laporan_delete, name='laporan-delete'),
    # path('<slug:slug>/upload', views.laporan_upload, name='laporan-upload'),
    # path('<slug:slug>/upload/edit/<int:pk>', views.laporan_upload_edit, name='laporan-upload-edit'),
    # path('<slug:slug>/upload/delete/<int:pk>', views.laporan_upload_delete, name='laporan-upload-delete'),
]
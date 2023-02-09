from django.urls import path
from osn import views

app_name = 'osn'
urlpatterns = [
    path('', views.index, name='osn-index'),
    path('input', views.bidang_osn_input, name='bidang-osn-input'),
    path('edit/<int:pk>', views.bidang_osn_edit, name='bidang-osn-edit'),
    path('delete/<int:pk>', views.bidang_osn_delete, name='bidang-osn-delete'),
    path('<slug:slug>', views.detail_bidang_osn, name='detail-bidang-osn'),
    path('<slug:slug>/input/siswa', views.siswa_osn_input, name='siswa-osn-input'),
    path('<slug:slug>/delete/siswa/<int:pk>', views.siswa_osn_delete, name='siswa-osn-delete'),
    path('<slug:slug>/input/laporan', views.laporan_osn_input, name='laporan-osn-input'),
    path('<slug:slug>/edit/laporan/<int:pk>', views.laporan_osn_edit, name='laporan-osn-edit'),
    path('<slug:slug>/delete/laporan/<int:pk>', views.laporan_osn_delete, name='laporan-osn-delete'),
]
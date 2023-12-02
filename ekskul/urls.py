from django.urls import path
from ekskul import views

app_name = 'ekskul'
urlpatterns = [
    path('', views.EkskulIndexView.as_view(), name='data-index'),
    path('santri/', views.DataSantriView.as_view(), name='data-santri'),
    path('<slug:slug>/', views.EkskulDetailView.as_view(), name='data-detail'),
    path('<slug:slug>/edit', views.UpdateEskkulView.as_view(), name='edit-detail'),
    path('<slug:slug>/input/anggota', views.InputAnggotaView.as_view(), name='input-anggota'),
    path('<slug:slug>/delete/anggota/<int:pk>', views.DeleteAnggotaView.as_view(), name='delete-anggota'),
    path('input/pembina', views.input_pembina, name='input-pembina'),

]
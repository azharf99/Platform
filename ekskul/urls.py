from django.urls import path
from ekskul import views

app_name = 'ekskul'
urlpatterns = [
    path('', views.EkskulIndexView.as_view(), name='data-index'),
    path('<slug:slug>/', views.EkskulDetailView.as_view(), name='data-detail'),
    path('<slug:slug>/edit', views.edit_ekskul, name='edit-detail'),
    path('<slug:slug>/input/anggota', views.input_anggota, name='input-anggota'),
    path('<slug:slug>/delete/anggota/<int:pk>', views.delete_anggota, name='delete-anggota'),
    path('input/pembina', views.input_pembina, name='input-pembina'),

]
from django.urls import path
from inventaris import views

app_name='inventaris'
urlpatterns = [
    path('', views.index, name='inventaris-index'),
    path('input', views.inventaris_input, name='inventaris-input'),
    path('edit/<int:pk>', views.inventaris_edit, name='inventaris-edit'),
    path('delete/<int:pk>', views.inventaris_delete, name='inventaris-delete'),
    path('detail/<int:pk>', views.inventaris_detail, name='inventaris-detail'),
]
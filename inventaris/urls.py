from django.urls import path
from inventaris import views

app_name='inventaris'
urlpatterns = [
    path('', views.index, name='inventaris-index'),
    path('input', views.inventaris_input, name='inventaris-input'),
    path('edit/<int:pk>', views.inventaris_edit, name='inventaris-edit'),
    path('delete/<int:pk>', views.inventaris_delete, name='inventaris-delete'),
    path('detail/<int:pk>', views.inventaris_detail, name='inventaris-detail'),
    path('status/input', views.inventaris_status_input, name='inventaris-status-input'),
    path('status/edit/<int:pk>', views.inventaris_status_edit, name='inventaris-status-edit'),
    path('status/delete/<int:pk>', views.inventaris_status_delete, name='inventaris-status-delete'),
    path('status/detail/<int:pk>', views.inventaris_status_detail, name='inventaris-status-detail'),
    path('invoice/input', views.inventaris_invoice_input, name='inventaris-invoice-input'),
    path('invoice/edit/<int:pk>', views.inventaris_invoice_edit, name='inventaris-invoice-edit'),
    path('invoice/delete/<int:pk>', views.inventaris_invoice_delete, name='inventaris-invoice-delete'),
    path('invoice/detail/<int:pk>', views.inventaris_invoice_detail, name='inventaris-invoice-detail'),
]
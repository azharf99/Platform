from django.urls import path
from inventaris import views

app_name='inventaris'
urlpatterns = [
    path('', views.index, name='inventaris-index'),
    path('input', views.inventaris_input, name='inventaris-input'),
]
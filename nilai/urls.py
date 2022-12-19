from django.urls import path
from nilai import views

app_name = 'nilai'
urlpatterns = [
    path('', views.index, name='nilai-index'),
    path('<slug:slug>', views.nilai_detail, name='nilai-detail'),
    path('<slug:slug>/input', views.nilai_input, name='nilai-input'),
]
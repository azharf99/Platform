from django.urls import path
from nilai import views

urlpatterns = [
    path('', views.index, name='nilai-index'),
]
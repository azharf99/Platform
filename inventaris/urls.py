from django.urls import path
from inventaris import views


urlpatterns = [
    path('', views.index, name='inventaris-index'),
]
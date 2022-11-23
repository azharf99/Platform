from django.urls import path
from proposal import views

urlpatterns = [
    path('', views.index, name='proposal')
]
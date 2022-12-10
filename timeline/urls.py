from django.urls import path
from timeline import views


urlpatterns = [
    path('', views.index, name='timeline-index'),
]
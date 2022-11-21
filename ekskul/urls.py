from django.urls import path
from ekskul import views

urlpatterns = [
    path('', views.home, name='home'),

]
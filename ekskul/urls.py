from django.urls import path
from ekskul import views

urlpatterns = [
    path('', views.home, name='data-index'),
    path('<int:pk>/', views.data_detail, name='data-detail'),

]
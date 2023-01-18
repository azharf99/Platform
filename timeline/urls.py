from django.urls import path
from timeline import views


urlpatterns = [
    path('', views.CalendarView.as_view(), name='timeline-index'),
]
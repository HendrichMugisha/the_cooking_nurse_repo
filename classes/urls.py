from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('classes/', views.class_timetable, name='class_timetable'),
]

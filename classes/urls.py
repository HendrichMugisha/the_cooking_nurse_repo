from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('classes/', views.class_timetable, name='class_timetable'),
    path('course/play/<slug:course_slug>/', views.online_class_player, name='online_class_player'),
]

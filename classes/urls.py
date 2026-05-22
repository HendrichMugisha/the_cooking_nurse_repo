from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('classes/', views.class_timetable, name='class_timetable'),
    path('course/play/<slug:course_slug>/', views.online_class_player, name='online_class_player'),
    path('classes/studio-rental/', views.studio_rental_request, name='studio_rental_request'),
]

from django.shortcuts import render
from .models import ClassSession

def class_timetable(request):
    sessions = ClassSession.objects.filter(course__is_active=True).order_by('date', 'start_time')
    return render(request, 'classes/class_timetable.html', {'sessions': sessions})

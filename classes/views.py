from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from orders.models import OrderItem
from .models import Course, ClassSession

def class_timetable(request):
    sessions = ClassSession.objects.filter(course__is_active=True).order_by('date', 'start_time')
    return render(request, 'classes/class_timetable.html', {'sessions': sessions})

@login_required
def online_class_player(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, course_type='online')
    
    # Verify user purchased this course
    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        online_course=course
    ).exists()
    
    if not has_purchased:
        raise Http404("You do not have access to this online course.")
        
    return render(request, 'classes/video_player.html', {'course': course})


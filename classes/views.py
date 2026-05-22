from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from orders.models import OrderItem
from portfolio.models import SiteSettings
from .models import Course, ClassSession
from decimal import Decimal
from datetime import datetime

def class_timetable(request):
    sessions = ClassSession.objects.filter(course__is_active=True).order_by('date', 'start_time')
    online_courses = Course.objects.filter(is_active=True, course_type='online')
    settings = SiteSettings.get_settings()
    return render(request, 'classes/class_timetable.html', {
        'sessions': sessions, 
        'online_courses': online_courses,
        'settings': settings
    })

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


from django.shortcuts import redirect
from django.contrib import messages
from users.forms import StudioBookingForm
from .models import StudioRentalPricing

@login_required
def studio_rental_request(request):
    pricing = StudioRentalPricing.load()
    if request.method == 'POST':
        form = StudioBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            # Calculate total price
            start_dt = datetime.combine(booking.date, booking.start_time)
            end_dt = datetime.combine(booking.date, booking.end_time)
            diff_hours = (end_dt - start_dt).total_seconds() / 3600.0
            booking.total_price = pricing.hourly_rate * Decimal(diff_hours)
            booking.save()
            
            messages.success(request, "Your studio rental request has been submitted! We will review it shortly.")
            return redirect('users:dashboard')
    else:
        form = StudioBookingForm()
        
    return render(request, 'classes/studio_rental.html', {'form': form, 'pricing': pricing})


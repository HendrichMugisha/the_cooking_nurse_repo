from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber

def home(request):
    return render(request, 'portfolio/home.html')

@require_POST
def newsletter_subscribe(request):
    email = request.POST.get('email', '').strip()
    if email:
        try:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Thank you for subscribing to our culinary wellness newsletter!")
            else:
                messages.info(request, "You are already subscribed to our newsletter.")
        except Exception:
            messages.error(request, "An error occurred. Please try again.")
            
    # Redirect back to where they came from
    next_url = request.POST.get('next', 'portfolio:home')
    return redirect(next_url)


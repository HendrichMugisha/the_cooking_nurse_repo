from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
import json

from classes.models import ClassSession, StudioRentalPricing
from catalog.models import Product
from .models import NewsletterSubscriber, SiteSettings

import re

def _extract_youtube_video_id(url):
    """Extract an 11-character YouTube video ID from any common YouTube URL format."""
    if not url:
        return None
    patterns = [
        r'(?:youtube(?:-nocookie)?\.com/watch\?v=|youtube(?:-nocookie)?\.com/embed/|youtube(?:-nocookie)?\.com/live/|youtu\.be/|youtube(?:-nocookie)?\.com/v/|youtube(?:-nocookie)?\.com/shorts/)([a-zA-Z0-9_-]{11})',
        r'[?&]v=([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    # Last resort: if the entire string is an 11-char ID
    stripped = url.strip()
    if re.match(r'^[a-zA-Z0-9_-]{11}$', stripped):
        return stripped
    return None

def home(request):
    settings = SiteSettings.get_settings()
    next_session = ClassSession.objects.filter(
        course__is_active=True, date__gte=timezone.now().date()
    ).order_by('date', 'start_time').first()
    has_classes = next_session is not None

    # Fresh Pickens: 4 newest active physical products with stock
    featured_products = Product.objects.filter(
        is_active=True, product_type='physical',
        variants__stock__gt=0
    ).distinct().order_by('-created_at')[:4]

    # Digital cookbooks count
    digital_count = Product.objects.filter(is_active=True, product_type='digital').count()

    # Studio pricing
    studio_pricing = StudioRentalPricing.load()

    # Parse loop words
    loop_words = [w.strip() for w in settings.hero_loop_words.split(',') if w.strip()] if settings.hero_loop_words else []

    # Check and pop session variable for lead magnet download
    download_lead_magnet = request.session.pop('download_lead_magnet', False)

    # Extract YouTube video ID server-side (avoids all client-side parsing/escaping issues)
    youtube_video_id = _extract_youtube_video_id(settings.featured_youtube_embed_url)

    context = {
        'settings': settings,
        'next_session': next_session,
        'has_classes': has_classes,
        'featured_products': featured_products,
        'digital_count': digital_count,
        'studio_pricing': studio_pricing,
        'loop_words_json': json.dumps(loop_words),
        'download_lead_magnet': download_lead_magnet,
        'youtube_video_id': youtube_video_id,
    }
    return render(request, 'portfolio/home.html', context)

@require_POST
def newsletter_subscribe(request):
    email = request.POST.get('email', '').strip()
    settings = SiteSettings.get_settings()
    if email:
        try:
            _, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                if settings.newsletter_lead_magnet:
                    messages.success(request, f"Thank you for subscribing! Your free download of '{settings.newsletter_lead_magnet_title}' will begin shortly.")
                    request.session['download_lead_magnet'] = True
                else:
                    messages.success(request, "Thank you for subscribing to our wholesome culinary newsletter!")
            else:
                messages.info(request, "You are already subscribed to our newsletter.")
        except Exception as e:
            messages.error(request, "An error occurred. Please try again.")
            
    # Redirect back to where they came from
    next_url = request.POST.get('next', 'portfolio:home')
    return redirect(next_url)

def studio_rental(request):
    if request.method == 'POST':
        # Capture lead and simulate email sending for MVP
        name = request.POST.get('name')
        messages.success(request, f"Thank you {name}, your inquiry has been sent. We will get back to you with a quote shortly!")
        return redirect('portfolio:studio_rental')
    return render(request, 'portfolio/studio_rental.html')


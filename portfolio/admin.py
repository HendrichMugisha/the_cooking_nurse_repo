from django.contrib import admin
from .models import SiteSettings, NewsletterSubscriber


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Single-instance admin for global site configuration."""
    list_display = ('__str__',)
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_text', 'hero_video', 'hero_image', 'hero_loop_words'),
        }),
        ('Meet The Nurse', {
            'fields': ('nurse_name', 'nurse_bio', 'nurse_portrait'),
        }),
        ('Social Media & Video', {
            'fields': ('youtube_url', 'instagram_url', 'tiktok_url', 'featured_youtube_embed_url'),
            'description': 'For "Featured YouTube Embed URL", paste any standard YouTube video link (e.g. https://www.youtube.com/watch?v=XXXXXXXXXXX). The system will automatically extract the video ID.',
        }),
        ('Newsletter & Lead Magnet', {
            'fields': ('newsletter_lead_magnet', 'newsletter_lead_magnet_title'),
        }),
        ('Landing Page Card Images', {
            'fields': ('digital_library_image', 'cooking_classes_image', 'studio_rental_image'),
        }),
    )

    def has_add_permission(self, request):
        # Only allow one SiteSettings instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

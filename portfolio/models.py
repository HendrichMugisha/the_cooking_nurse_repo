from django.db import models

class SiteSettings(models.Model):
    hero_text = models.CharField(max_length=255, default="Turn Everyday Cooking into Everyday Magic!")
    hero_video = models.FileField(upload_to='site/', blank=True, null=True, help_text="Upload an mp4 video for the hero background")
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Fallback hero image (used if video fails or on mobile)")
    nurses_note = models.TextField(default="Tomatoes are rich in Lycopene...", help_text="Note to include in digital downloads and about section")
    
    # Typewriter loop keywords
    hero_loop_words = models.CharField(max_length=500, blank=True, default="Healing, Art, Joy, Nourishment",
        help_text="Comma-separated keywords for the typewriter loop (e.g. 'Healing, Art, Joy')")

    # Meet the Nurse
    nurse_name = models.CharField(max_length=100, blank=True, default="The Cooking Nurse")
    nurse_bio = models.TextField(blank=True, default="", help_text="Short bio for the Meet the Nurse section")
    nurse_portrait = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Portrait photo")
    nurse_subtitle = models.TextField(
        default="Discover the healing culinary philosophy, medical nutrition background, and heart-led mission of the nurse blending clinical science with sensory kitchen joy.",
        help_text="Introductory subtitle for the Meet the Chef section"
    )

    # Dynamic Landing Page Sections text
    homepage_about_title = models.CharField(
        max_length=255, default="Experience The Cooking Nurse",
        help_text="Title for the Experience section"
    )
    homepage_about_subtitle = models.TextField(
        default="Step into a sensory kitchen designed to feed your soul, strengthen your body, and inspire your everyday meals.",
        help_text="Subtitle/description for the Experience section"
    )

    # Social media links
    youtube_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    tiktok_url = models.URLField(blank=True, default="")
    featured_youtube_embed_url = models.URLField(blank=True, default="",
        help_text="Paste a YouTube video URL to embed (e.g. https://youtube.com/watch?v=...)")

    # Newsletter lead magnet
    newsletter_lead_magnet = models.FileField(upload_to='site/lead_magnets/', blank=True, null=True,
        help_text="Upload a free PDF to offer subscribers as incentive")
    newsletter_lead_magnet_title = models.CharField(max_length=200, blank=True, default="Free Wholesome Recipe Guide")

    # Landing Page Card Images
    digital_library_image = models.ImageField(upload_to='site/cards/', blank=True, null=True, help_text="Image for the Digital Library card")
    cooking_classes_image = models.ImageField(upload_to='site/cards/', blank=True, null=True, help_text="Image for the Cooking Classes card")
    studio_rental_image = models.ImageField(upload_to='site/cards/', blank=True, null=True, help_text="Image for the Studio Rental card")

    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Global Site Settings"
        
    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email

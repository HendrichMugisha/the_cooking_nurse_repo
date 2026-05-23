from django.db import models
from django.utils.text import slugify
from core.storage_backends import select_video_storage

class Course(models.Model):
    CLASS_TYPES = (
        ('physical', 'Physical In-Person Class'),
        ('online', 'Online Pre-recorded Class'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    course_type = models.CharField(max_length=10, choices=CLASS_TYPES, default='physical')
    description = models.TextField()
    image = models.ImageField(upload_to='classes/', blank=True, null=True)
    
    # Base price for the class
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Price in UGX")

    # Only used if course_type is 'online'
    video = models.FileField(upload_to='course_videos/', blank=True, null=True, storage=select_video_storage, help_text="Upload the class video file (e.g. mp4)")

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ClassSession(models.Model):
    """
    Specific dates for physical classes. Online classes don't need sessions.
    """
    course = models.ForeignKey(Course, related_name='sessions', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    capacity = models.PositiveIntegerField(default=10, help_text="Maximum number of attendees")
    attendees_count = models.PositiveIntegerField(default=0, help_text="Current number of bookings")

    def __str__(self):
        return f"{self.course.title} - {self.date}"

    @property
    def is_full(self):
        return self.attendees_count >= self.capacity

class StudioRentalPricing(models.Model):
    """
    Singleton model to hold the global hourly rate for studio rental.
    """
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=0, default=50000, help_text="Hourly rental rate in UGX")
    min_hours = models.PositiveIntegerField(default=2, help_text="Minimum hours required to book")

    def save(self, *args, **kwargs):
        self.pk = 1 # Ensure singleton
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"Studio Pricing ({self.hourly_rate} UGX/hr)"

class StudioBooking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved (Awaiting Payment)'),
        ('paid', 'Paid & Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='studio_bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.TextField(help_text="Brief description of the rental purpose (e.g. food photography, test kitchen)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rental on {self.date} by {self.user.email} ({self.status})"

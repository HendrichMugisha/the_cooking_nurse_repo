from django.db import models
from django.utils.text import slugify

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
    video_url = models.URLField(blank=True, null=True, help_text="Secure video link (e.g. Mux/Vimeo)")

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

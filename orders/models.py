from django.db import models
from django.conf import settings
from catalog.models import ProductVariant
from classes.models import Course, ClassSession

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('paid', 'Paid / Processing'),
        ('shipped', 'Out for Delivery'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    
    # Structured Delivery Fields (Ready for API integration later)
    street_address = models.CharField(max_length=255, blank=True, null=True, help_text="Fallback text address")
    city = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=100, blank=True, null=True)
    landmark_or_building = models.CharField(max_length=255, blank=True, null=True)
    delivery_notes = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    
    # Item can be a Product Variant OR an Online Course OR a Physical Class Session
    # For MVP, we will link them loosely or using specific nullable foreign keys
    product_variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL)
    online_course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    class_session = models.ForeignKey(ClassSession, null=True, blank=True, on_delete=models.SET_NULL)
    
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        if self.product_variant:
            return f"{self.quantity}x {self.product_variant.product.name}"
        elif self.online_course:
            return f"Online Class: {self.online_course.title}"
        elif self.class_session:
            return f"Booking: {self.class_session.course.title} on {self.class_session.date}"
        return "Unknown Item"

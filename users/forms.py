from django import forms
from django.forms import inlineformset_factory
from django.core.files.uploadedfile import UploadedFile
from catalog.models import Product, ProductVariant, Category
from classes.models import Course, ClassSession

class StyledModelForm(forms.ModelForm):
    """
    Base model form that automatically injects premium Tailwind CSS classes into fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Common premium Tailwind classes for inputs
            css_classes = "form-input w-full p-2.5 bg-surface-container-high border border-outline-variant rounded-lg text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200"
            
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = "h-5 w-5 rounded border-outline-variant text-primary focus:ring-primary/20 transition-all duration-200 cursor-pointer"
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = css_classes + " resize-y min-h-[100px]"
                field.widget.attrs['rows'] = 4
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = "file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-primary/10 file:text-primary hover:file:bg-primary/20 file:cursor-pointer transition-all duration-200"
            else:
                field.widget.attrs['class'] = css_classes

class ProductForm(StyledModelForm):
    class Meta:
        model = Product
        fields = ['categories', 'name', 'product_type', 'description', 'image', 'digital_file', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter product details, nutrition highlights...'}),
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Organic Honey Butter'}),
        }

class ProductVariantForm(StyledModelForm):
    class Meta:
        model = ProductVariant
        fields = ['name', 'sku', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "e.g. '500g', '1L', or 'Default'"}),
            'sku': forms.TextInput(attrs={'placeholder': "e.g. HN-BUT-500"}),
            'price': forms.NumberInput(attrs={'placeholder': "Price in UGX"}),
            'stock': forms.NumberInput(attrs={'placeholder': "Stock quantity"}),
        }

# Formset for Product Variants
ProductVariantFormSet = inlineformset_factory(
    Product, 
    ProductVariant, 
    form=ProductVariantForm, 
    extra=1, 
    can_delete=True,
    min_num=1,
    validate_min=True
)

class CourseForm(StyledModelForm):
    class Meta:
        model = Course
        fields = ['title', 'course_type', 'description', 'image', 'price', 'video', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Detail course syllabus, recipes covered...'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Clinical Nutrition in Italian Cooking'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price in UGX'}),
        }
        
    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video and isinstance(video, UploadedFile):
            if not video.name.lower().endswith('.mp4'):
                raise ValidationError("Only .mp4 video files are allowed.")
            if video.size > 500 * 1024 * 1024:
                raise ValidationError("Course video file size cannot exceed 500MB.")
        return video

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and isinstance(image, UploadedFile):
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image file size cannot exceed 5MB.")
        return image

class ClassSessionForm(StyledModelForm):
    class Meta:
        model = ClassSession
        fields = ['date', 'start_time', 'end_time', 'capacity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'capacity': forms.NumberInput(attrs={'placeholder': 'e.g. 15'}),
        }

# Formset for Course Sessions (Physical Classes)
ClassSessionFormSet = inlineformset_factory(
    Course, 
    ClassSession, 
    form=ClassSessionForm, 
    extra=1, 
    can_delete=True
)

class CategoryForm(StyledModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Artisanal Ghee'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional description of the category...'}),
        }

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = "form-input w-full p-2.5 bg-surface-container-high border border-outline-variant rounded-lg text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all duration-200"
            field.widget.attrs['class'] = css_classes

from portfolio.models import SiteSettings
from classes.models import StudioRentalPricing
from django.core.exceptions import ValidationError

class SiteSettingsForm(StyledModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'hero_text', 'hero_video', 'hero_image', 'nurses_note',
            'hero_loop_words', 'nurse_name', 'nurse_bio', 'nurse_portrait',
            'nurse_subtitle', 'homepage_about_title', 'homepage_about_subtitle',
            'facebook_url', 'twitter_url', 'instagram_url', 'tiktok_url', 'youtube_url', 'whatsapp_number', 'featured_youtube_embed_url',
            'newsletter_lead_magnet', 'newsletter_lead_magnet_title',
            'digital_library_image', 'cooking_classes_image', 'studio_rental_image'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # These fields have model-level defaults so they should not be
        # required at the form level — a blank submission should be valid.
        optional_fields = [
            'whatsapp_number', 'facebook_url', 'twitter_url', 'instagram_url',
            'tiktok_url', 'youtube_url', 'featured_youtube_embed_url',
            'hero_loop_words', 'nurse_name', 'nurse_bio', 'nurse_subtitle',
            'homepage_about_title', 'homepage_about_subtitle',
            'newsletter_lead_magnet_title', 'nurses_note', 'hero_text',
        ]
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False

    def clean_hero_video(self):
        video = self.cleaned_data.get('hero_video')
        if video and isinstance(video, UploadedFile):
            if not video.name.lower().endswith('.mp4'):
                raise ValidationError("Only .mp4 video files are allowed.")
            if video.size > 50 * 1024 * 1024:
                raise ValidationError("Video file size cannot exceed 50MB.")
        return video

    def clean_hero_image(self):
        image = self.cleaned_data.get('hero_image')
        if image and isinstance(image, UploadedFile):
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image file size cannot exceed 5MB.")
        return image

class StudioRentalPricingForm(StyledModelForm):
    class Meta:
        model = StudioRentalPricing
        fields = ['hourly_rate', 'min_hours']
        widgets = {
            'hourly_rate': forms.NumberInput(attrs={'placeholder': 'Price per hour in UGX'}),
            'min_hours': forms.NumberInput(attrs={'placeholder': 'Minimum booking hours required'}),
        }


from classes.models import StudioBooking
from datetime import datetime, date

class StudioBookingForm(StyledModelForm):
    class Meta:
        model = StudioBooking
        fields = ['date', 'start_time', 'end_time', 'purpose']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'purpose': forms.Textarea(attrs={'placeholder': 'e.g. Test kitchen, Food photography...', 'rows': 3}),
        }

    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date and booking_date < date.today():
            raise ValidationError("You cannot book a date in the past.")
        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        if start and end:
            if start >= end:
                raise ValidationError("End time must be after start time.")
            
            # Optionally validate min_hours
            from classes.models import StudioRentalPricing
            pricing = StudioRentalPricing.load()
            start_dt = datetime.combine(date.today(), start)
            end_dt = datetime.combine(date.today(), end)
            diff_hours = (end_dt - start_dt).total_seconds() / 3600.0
            
            if diff_hours < pricing.min_hours:
                raise ValidationError(f"Minimum booking time is {pricing.min_hours} hours.")
                
        return cleaned_data

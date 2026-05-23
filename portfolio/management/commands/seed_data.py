import os
from django.core.management.base import BaseCommand
from django.core.files import File
from users.models import CustomUser
from portfolio.models import SiteSettings
from catalog.models import Category, Product, ProductVariant
from classes.models import Course, ClassSession, StudioRentalPricing
from datetime import date, timedelta, time

class Command(BaseCommand):
    help = 'Seeds the database with test items for The Cooking Nurse application'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seeding...")

        # 1. USERS
        if not CustomUser.objects.filter(email='admin@test.com').exists():
            CustomUser.objects.create_superuser('admin@test.com', 'adminpass123')
            self.stdout.write("Created superuser admin@test.com")
        
        if not CustomUser.objects.filter(email='user@test.com').exists():
            CustomUser.objects.create_user('user@test.com', 'userpass123')
            self.stdout.write("Created test user user@test.com")

        # 2. STUDIO PRICING
        pricing = StudioRentalPricing.load()
        pricing.hourly_rate = 50000
        pricing.min_hours = 2
        pricing.save()
        self.stdout.write("Configured Studio Pricing")

        # 3. SETTINGS
        settings = SiteSettings.get_settings()
        settings.hero_text = "Turn Everyday Cooking into Everyday Magic!"
        settings.nurse_name = "Ritah Tumuhimbise"
        settings.nurse_bio = "A popular Ugandan food content creator, chef, and registered nurse."
        settings.youtube_url = "https://youtube.com/@TheCookingNurse"
        settings.featured_youtube_embed_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        settings.save()
        self.stdout.write("Configured Site Settings")

        # 4. CATEGORIES
        cat_ghee, _ = Category.objects.get_or_create(name="Artisanal Ghee")
        cat_produce, _ = Category.objects.get_or_create(name="Fresh Produce")
        cat_books, _ = Category.objects.get_or_create(name="E-Books")

        # 5. PRODUCTS
        ghee_path = r"C:\Users\casus\.gemini\antigravity-ide\brain\078f6e4a-f2d2-4a7d-bf81-f160053e26df\organic_farm_ghee_1779457680071.png"
        matooke_path = r"C:\Users\casus\.gemini\antigravity-ide\brain\078f6e4a-f2d2-4a7d-bf81-f160053e26df\fresh_matooke_1779457697811.png"
        ebook_path = r"C:\Users\casus\.gemini\antigravity-ide\brain\078f6e4a-f2d2-4a7d-bf81-f160053e26df\meal_plan_ebook_1779457713945.png"

        # Ghee
        ghee, created = Product.objects.get_or_create(name="Organic Farm Ghee", product_type="physical")
        if created:
            ghee.description = "Pure, unadulterated artisanal ghee sourced from organic Ugandan farms."
            if os.path.exists(ghee_path):
                with open(ghee_path, 'rb') as f:
                    ghee.image.save("ghee.png", File(f))
            ghee.categories.add(cat_ghee)
            ProductVariant.objects.create(product=ghee, name="500ml", price=25000, stock=50)
            ProductVariant.objects.create(product=ghee, name="1 Kg", price=45000, stock=30)
            self.stdout.write("Created Ghee product")

        # Matooke
        matooke, created = Product.objects.get_or_create(name="Fresh Matooke Bundle", product_type="physical")
        if created:
            matooke.description = "A fresh, green bundle of premium matooke, perfect for traditional steaming."
            if os.path.exists(matooke_path):
                with open(matooke_path, 'rb') as f:
                    matooke.image.save("matooke.png", File(f))
            matooke.categories.add(cat_produce)
            ProductVariant.objects.create(product=matooke, name="Default Bundle", price=15000, stock=100)
            self.stdout.write("Created Matooke product")

        # E-book
        ebook, created = Product.objects.get_or_create(name="7-Day Wholesome Meal Plan", product_type="digital")
        if created:
            ebook.description = "An extensive digital guide with recipes and meal preps for a week of wholesome cooking."
            if os.path.exists(ebook_path):
                with open(ebook_path, 'rb') as f:
                    ebook.image.save("meal_plan.png", File(f))
            ebook.categories.add(cat_books)
            ProductVariant.objects.create(product=ebook, name="Digital Download", price=50000, stock=0)
            self.stdout.write("Created Ebook product")

        # 6. CLASSES
        class_path = r"C:\Users\casus\.gemini\antigravity-ide\brain\078f6e4a-f2d2-4a7d-bf81-f160053e26df\cooking_class_1779457732991.png"

        course, created = Course.objects.get_or_create(title="Mastering Local Cuisine", course_type="physical", price=150000)
        if created:
            course.description = "Join us in our studio kitchen to learn how to prepare authentic, wholesome local dishes."
            if os.path.exists(class_path):
                with open(class_path, 'rb') as f:
                    course.image.save("class.png", File(f))
            
            # Create a session 7 days from now
            session_date = date.today() + timedelta(days=7)
            ClassSession.objects.create(
                course=course,
                date=session_date,
                start_time=time(14, 0),
                end_time=time(17, 0),
                capacity=12,
                attendees_count=5
            )
            self.stdout.write("Created Course and Session")

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))

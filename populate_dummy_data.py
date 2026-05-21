import os
import django
from datetime import date, time, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from catalog.models import Category, Product, ProductVariant
from classes.models import Course, ClassSession

def populate():
    print("Clearing old data...")
    Category.objects.all().delete()
    Product.objects.all().delete()
    Course.objects.all().delete()

    print("Creating Categories...")
    cat_groceries = Category.objects.create(name="Groceries", description="Fresh and organic supplies.")
    cat_digital = Category.objects.create(name="Digital Cookbooks", description="Downloadable recipe books.")

    print("Creating Products & Variants...")
    p1 = Product.objects.create(
        category=cat_groceries,
        name="Heirloom Tomato Harvest",
        product_type="physical",
        description="Sustainably grown, sun-ripened organic tomatoes from our heritage vines. Perfect for slicing, roasting, or enjoying fresh with sea salt."
    )
    ProductVariant.objects.create(product=p1, name="1 Kg Box", price=12000, stock=50)
    ProductVariant.objects.create(product=p1, name="2 Kg Box", price=22000, stock=30)

    p2 = Product.objects.create(
        category=cat_groceries,
        name="Pure Artisanal Ghee",
        product_type="physical",
        description="Traditional, clarified butter made from grass-fed cows. Perfect for authentic local dishes."
    )
    ProductVariant.objects.create(product=p2, name="500ml Jar", price=25000, stock=20)
    ProductVariant.objects.create(product=p2, name="1L Jar", price=45000, stock=15)

    p3 = Product.objects.create(
        category=cat_digital,
        name="The Everyday Magic Cookbook",
        product_type="digital",
        description="A complete digital guide to making 50 quick, healthy, and delicious meals."
    )
    ProductVariant.objects.create(product=p3, name="Digital Download", price=50000, stock=999)

    print("Creating Courses & Sessions...")
    c1 = Course.objects.create(
        title="Breakfast Dishes & Meal Planning",
        course_type="physical",
        description="Learn to make 3 eggs dishes, 2 katogos, pancakes, and perfect your morning routine.",
        price=150000
    )
    ClassSession.objects.create(
        course=c1,
        date=date.today() + timedelta(days=5),
        start_time=time(9, 0),
        end_time=time(17, 0),
        capacity=10
    )

    c2 = Course.objects.create(
        title="Local Food Masterclass",
        course_type="physical",
        description="Master Matooke, Karo, Eshabwe, and authentic Luwombo preparations.",
        price=150000
    )
    ClassSession.objects.create(
        course=c2,
        date=date.today() + timedelta(days=12),
        start_time=time(9, 0),
        end_time=time(18, 0),
        capacity=12
    )

    c3 = Course.objects.create(
        title="Artisanal Sourdough & Gut Health",
        course_type="online",
        description="An extensive 2-hour pre-recorded masterclass on advanced fermentation techniques.",
        price=85000,
        video_url="https://vimeo.com/placeholder"
    )

    print("Dummy data successfully populated!")

if __name__ == '__main__':
    populate()

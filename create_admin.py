import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser(email='admin@example.com', password='adminpassword')
    print("Superuser created successfully!")
    print("Email: admin@example.com")
    print("Password: adminpassword")
else:
    print("Superuser admin@example.com already exists.")

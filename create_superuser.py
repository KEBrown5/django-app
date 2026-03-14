# create_superuser.py
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogsite.settings")
django.setup()

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@gmail.com", "Abooten614")
    print("Superuser created!")
else:
    print("Superuser already exists.")
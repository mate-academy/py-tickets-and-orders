import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "django-insecure-mate-academy-tickets-and-orders"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "db",
]

AUTH_USER_MODEL = "db.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TIME_ZONE = "UTC"

USE_TZ = False

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "test-secret-key"

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

USE_TZ = False

# Django 5 does NOT auto-create tables for apps without migrations
MIGRATION_MODULES = {
    "db": None,
}

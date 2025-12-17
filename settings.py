from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

USE_TZ = False

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "db",
]

AUTH_USER_MODEL = "db.User"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

SECRET_KEY = "django-insecure-test-key"

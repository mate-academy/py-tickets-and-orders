from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    # ... inne aplikacje
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "db", # Twoja aplikacja z modelami
    # ...
]

AUTH_USER_MODEL = "db.User"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


INSTALLED_APPS = [
    "db",
    "django.contrib.auth",
    "django.contrib.contenttypes",
]


AUTH_USER_MODEL = "db.User"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Kiev"
USE_I18N = True

USE_TZ = False

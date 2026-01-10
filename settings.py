import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = "6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

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

# ↓↓↓ ADICIONE ESTAS CONFIGURAÇÕES AO SEU INSTALLED_APPS ↓↓↓
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",           # ← ADICIONE
    "django.contrib.contenttypes",   # ← ADICIONE
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "db",                            # ← JÁ ESTAVA AQUI
]

# ↓↓↓ ADICIONE ESTA LINHA NO FINAL DO ARQUIVO ↓↓↓
AUTH_USER_MODEL = "db.User"

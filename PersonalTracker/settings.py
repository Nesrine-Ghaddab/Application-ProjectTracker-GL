# settings.py - cleaned single-source configuration

import os
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-placeholder")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if not DEBUG else []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'rest_framework',
    'resend',
    'PersonalTracker',
    'Reunion',
    'UserApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PersonalTracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PersonalTracker.wsgi.application'

# Database (keep your existing settings if different)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validators (keep as-is)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization / Timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Africa/Tunis"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-crontab jobs
CRONJOBS = [
    ('*/1 * * * *', 'Reunion.cron.send_reminders'),           # Run every minute
    ('*/5 * * * *', 'Reunion.cron.auto_generate_recurring_meetings'),  # Run every 5 minutes
]

BASE_DIR = Path(__file__).resolve().parent.parent
# remove or change custom user
# AUTH_USER_MODEL = "UserApp.User"
AUTH_USER_MODEL = "auth.User"
SILENCED_SYSTEM_CHECKS = ['fields.E304']


# Email (Gmail SMTP)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = "masteroogway2024@gmail.com"
EMAIL_HOST_PASSWORD = "baih mgjw okdf nbcv"   # the 16-char App Password exactly as Google showed (including spaces)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

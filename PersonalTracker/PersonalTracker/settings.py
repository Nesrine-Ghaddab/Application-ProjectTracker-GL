from pathlib import Path

# ------------------ PATHS ------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------ SECURITY ------------------
SECRET_KEY = "CHANGE-THIS-KEY-IN-PRODUCTION"

DEBUG = True

ALLOWED_HOSTS = []


# ------------------ APPS ------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_crontab",

    # Local apps
    "UserApp",
    "SessionApp",
    "Reunion",
    "Gestion_Projects",

    # External apps
    "captcha",
]


# ------------------ MIDDLEWARE ------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ------------------ URLS ------------------
ROOT_URLCONF = "PersonalTracker.urls"


# ------------------ TEMPLATES ------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.parent / "templates",   # corrected template path
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ------------------ WSGI ------------------
WSGI_APPLICATION = "PersonalTracker.wsgi.application"


# ------------------ DATABASE ------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ------------------ PASSWORD VALIDATION ------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ------------------ LANGUAGE & TIME ------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ------------------ STATIC FILES ------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"


# ------------------ MEDIA FILES ------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ------------------ USER MODEL ------------------
AUTH_USER_MODEL = "UserApp.User"


# ------------------ EMAIL ------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ------------------ CAPTCHA CONFIG ------------------
CAPTCHA_FONT_SIZE = 40
CAPTCHA_LENGTH = 6
# Email (Gmail SMTP)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = "masteroogway2024@gmail.com"
EMAIL_HOST_PASSWORD = "baih mgjw okdf nbcv"   # the 16-char App Password exactly as Google showed (including spaces)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#cron
# django-crontab jobs
CRONJOBS = [
    ('*/1 * * * *', 'Reunion.cron.send_reminders'),           # Run every minute
    ('*/5 * * * *', 'Reunion.cron.auto_generate_recurring_meetings'),  # Run every 5 minutes
]
# Internationalization / Timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Africa/Tunis"
USE_I18N = True
USE_TZ = True

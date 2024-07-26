from pathlib import Path
import environ
import os

# Config environment varaibles
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = env("DEBUG")

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")


ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOGIN_URL = "/accounts/login/"

THRID_PARTY_APPS = [
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # # social media apps
    # 'allauth.socialaccount.providers.google',
    "crispy_forms",
    "crispy_bootstrap4",
]

LOCAL_APPS = [
    "apps.users.apps.UsersConfig",
    "apps.core.apps.CoreConfig",
    "apps.profiles.apps.ProfilesConfig",
    # "apps.classes.apps.ClassesConfig",
    "apps.reports.apps.ReportsConfig",
    "apps.teachers.apps.TeachersConfig",
    "apps.staff.apps.StaffConfig",
    "apps.fees.apps.FeesConfig",
    "apps.students.apps.StudentsConfig",
    "apps.terms.apps.TermsConfig",
    "apps.settings.apps.SettingsConfig",
    "apps.announcements.apps.AnnouncementsConfig",
    "apps.attendance.apps.AttendanceConfig",
    "apps.leave.apps.LeaveConfig",
    "apps.scelery.apps.SceleryConfig",
]


INSTALLED_APPS = DJANGO_APPS + THRID_PARTY_APPS + LOCAL_APPS

CRISPY_TEMPLATE_PACK = "bootstrap4"


MIDDLEWARE = [
    "apps.common.middleware.CheckSetupMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "sms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                # 'django.template.context_processossages",rs.request',
            ],
        },
    },
]

WSGI_APPLICATION = "sms.wsgi.application"


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# USER RELATED CONFIGURATIONS
AUTH_USER_MODEL = "users.User"


# LOGGING
import logging
import logging.config
from django.utils.log import DEFAULT_LOGGING

logger = logging.getLogger(__name__)
LOG_FILE_NAME = "sms.log"
LOG_LEVEL = "INFO"


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
            },
            "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "console"},
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "formatter": "file",
                "filename": f"logs/{LOG_FILE_NAME}",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            "": {"level": "INFO", "handlers": ["console", "file"], "propagate": False},
            "apps": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)


CELERY_BROKER_URL = "redis://localhost:6379/0"

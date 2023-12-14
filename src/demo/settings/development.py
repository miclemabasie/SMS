from .base import *


DEVELOPMENT_APPS = [
    "debug_toolbar",
    "django_extensions",
]

INSTALLED_APPS += DEVELOPMENT_APPS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# DATABASE SETTINGS FOR LOCAL DEVELOPMENT

# -------- Defaul database config ---------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -------Database config for postgresql or mysql --------

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env("PG_NAME"),
#         "USER": env("PG_USER"),
#         "PASSWORD": env("PG_PASSWORD"),
#         "HOST": env("PG_HOST"),
#         "PORT": env("PG_PORT"),
#     }
# }


# DJANGO DEBUG TOOLBAR CONFIGURATION

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

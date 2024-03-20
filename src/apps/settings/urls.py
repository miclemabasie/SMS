from django.urls import path
from . import views

app_name = "settings"


urlpatterns = [
    path("", views.settings_view, name="settings-home"),
    path("sessions/", views.session_settings_view, name="setting-sessions"),
    path("terms/", views.term_settings_view, name="setting-terms"),
]
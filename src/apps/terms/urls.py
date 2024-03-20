from django.urls import path
from . import views

app_name = "sessions"


urlpatterns = [
    path("create-session", views.create_academic_year, name="session-create"),
    path("edit-session/<int:pkid>/", views.edit_academic_year, name="session-edit"),
    path("mark-session-active/<int:pkid>/", views.mark_session_as_active, name="session-mark-active"),
]
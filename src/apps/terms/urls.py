from django.urls import path
from . import views

app_name = "sessions"


urlpatterns = [
    path("create-session", views.create_academic_year, name="session-create"),
    path("edit-session/<int:pkid>/", views.edit_academic_year, name="session-edit"),
    path("mark-session-active/<int:pkid>/", views.mark_session_as_active, name="session-mark-active"),

    path("create-term", views.create_term_view, name="term-create"),
    path("edit-term/<int:pkid>/", views.edit_term_view, name="term-edit"),
    path("mark-term-active/<int:pkid>/", views.mark_term_as_active, name="term-mark-active"),

    path("create-exam-session/", views.add_exam_session_view, name="exam-session-add"),
    path("edit-exam-session/<int:pkid>/", views.edit_exam_session_view, name="exam-session-edit"),
    path("mark-exam-session/<int:pkid>/", views.mark_exam_session_as_current_view, name="exam-session-mark-active")
]

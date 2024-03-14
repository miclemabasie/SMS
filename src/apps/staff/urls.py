from django.urls import path
from . import views


app_name = "staff"

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),



    # Subjects.
    path("subjects/", views.list_all_subjects, name="subjects"),
    path("assign-subjects/<int:pkid>/", views.assign_subject_to_classes, name="subjects-assign"),
]
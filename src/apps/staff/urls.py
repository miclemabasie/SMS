from django.urls import path
from . import views


app_name = "staff"

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),

    # Subjects.
    path("subjects/", views.list_all_subjects, name="subjects"),
    path("subjects/delete/<int:pkid>/", views.delete_subject, name="subjects-delete"),
    path("add-subjects", views.add_subject_view, name="subject-add"),
    path("edit-subjects/<int:pkid>/", views.edit_subject_view, name="subject-edit"),
    path("assign-subjects/<int:pkid>/", views.assign_subject_to_classes, name="subjects-assign"),
]
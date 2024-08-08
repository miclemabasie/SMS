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
    path(
        "assign-subjects/<int:pkid>/",
        views.assign_subject_to_classes,
        name="subjects-assign",
    ),
    path("create-admin", views.create_staff, name="create-admin"),
    path("list", views.list_admin, name="list-admin"),
    path("admin-marks", views.mark_list_admin_view, name="admin-marks"),
    path(
        "subject-marks-list/<int:class_pkid>/",
        views.subject_marks_list,
        name="subject-marks-list",
    ),
    path(
        "staff-upload-marks-file/<int:subject_pkid>/<int:class_pkid>/",
        views.staff_upload_marks,
        name="staff-upload-marks-file",
    ),
    path(
        "download-sample-subjects-file",
        views.download_sample_subject_file,
        name="download-sample-subjects-file",
    ),
    path(
        "upload-subjects-from-file",
        views.upload_subjects_from_file,
        name="upload-subjects-from-file",
    ),
]

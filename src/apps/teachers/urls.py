from django.urls import path

from . import views

app_name = "teachers"

urlpatterns = [
    path("", views.teacher_list_view, name="teachers-list"),
    path("add", views.teacher_add_view, name="teachers-add"),
    path(
        "<int:pkid>/<str:matricule>/", views.teacher_detail_view, name="teachers-detail"
    ),
    path(
        "edit/<int:pkid>/<str:matricule>/",
        views.teacher_edit_view,
        name="teachers-edit",
    ),
    path(
        "delete/<int:pkid>/<str:matricule>/",
        views.teacher_delete_view,
        name="teachers-delete",
    ),
    path("verify-teacher", views.verify_teacher_pin, name="verify_pin"),
    path("teacher-dashboard", views.teacher_dashboard, name="teacher-dashboard"),
    # assign subjects
    path(
        "assign-subjects/<int:teacher_pkid>/<str:teacher_mat>/",
        views.assign_class_to_teacher,
        name="assign-subjects",
    ),
    path(
        "download-form",
        views.download_blank_teacher_form,
        name="download-teacher-form",
    ),
    path(
        "download-teacher-list",
        views.download_teacher_list,
        name="download-teacher-list",
    ),
    path("upload-teachers", views.upload_teachers_from_file, name="upload-teachers"),
    path(
        "download-teacher-sample-file",
        views.download_teacher_sample_file,
        name="download-teacher-sample-file",
    ),
]

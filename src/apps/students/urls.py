from django.urls import path
from . import views

app_name = "students"


urlpatterns = [
    path("", views.list_student_view, name="student-list"),
    path(
        "<int:pkid>/<str:matricule>/", views.student_detail_view, name="student-detail"
    ),
    path(
        "edit/<int:pkid>/<str:matricule>/",
        views.edit_student_profile,
        name="student-edit",
    ),
    # path("delete/<int:pkid>/<str:matricule>/", views.delete, name="student-edit"),
    path(
        "student-record/<int:pkid>/<str:matricule>/",
        views.list_student_record,
        name="student-academic-record",
    ),
    path("add/", views.add_student_view, name="student-add"),
    path(
        "assign-optional-subjects/<int:student_pkid>/<str:student_matricule>/",
        views.add_optional_subjects_to_student,
        name="assign-optional-subjects",
    ),
    path(
        "download-class-list/",
        views.download_class_list,
        name="download-class-list",
    ),
    path(
        "upload-students/",
        views.upload_students_from_file,
        name="upload-students-from-file",
    ),
    path(
        "download-sample-file",
        views.download_sample_student_file,
        name="download-sample-file",
    ),
    # Marks
    path(
        "download-marks-sheet/<int:class_pkid>/",
        views.download_marksheet,
        name="mark-sheet-download",
    ),
    path("upload-marks/<int:class_pkid>", views.upload_marks, name="marks-upload"),
    path("marks", views.marks, name="marks"),
]

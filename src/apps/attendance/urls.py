from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("take-attendance", views.take_attendance, name="take-attendance"),
    path("get-students", views.get_students, name="get-students"),
    path("save-attendance", views.save_attendance, name="save_attendance"),
    path("view-attendance", views.view_attendance, name="view-attendance"),
    path("get-attendance", views.get_attendance, name="get_attendance"),
    path(
        "get-student-attendance",
        views.get_student_attendance,
        name="get_student_attendance",
    ),
    path("update_attendance", views.update_attendance, name="update_attendance"),
]

from django.urls import path
from . import views

app_name = "students"


urlpatterns = [
    path("", views.list_student_view, name="student-list"),
    path("<int:pkid>/<str:matricule>/", views.student_detail_view, name="student-detail"),
    path("edit/<int:pkid>/<str:matricule>/", views.edit_student_profile, name="student-edit"),
    path("add/", views.add_student_view, name="student-add"),
]
from django.urls import path
from . import views

app_name = "students"


urlpatterns = [
    path("", views.list_student_view, name="student-list"),
    path("<int:pkid>/<str:matricule>/", views.student_detail_view, name="student-detail"),
    path("add/", views.add_student_view, name="student-add")
]
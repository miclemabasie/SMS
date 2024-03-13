from django.urls import path
from . import views


app_name = "staff"

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),

    # Subjects.
    path("subjects/", views.list_all_subjects, name="subjects"),
]
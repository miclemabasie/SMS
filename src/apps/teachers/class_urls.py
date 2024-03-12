from django.urls import path

from . import views


app_name = "teachers"

urlpatterns = [
    path("add-class/", views.class_add_view, name="classes-add")
]
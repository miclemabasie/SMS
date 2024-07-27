from django.urls import path

from . import views

app_name = "scelery"

urlpatterns = [
    path("", views.form_view, name="form"),
]

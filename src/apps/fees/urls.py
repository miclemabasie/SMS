from django.urls import path

from . import views

app_name = "fees"

urlpatterns = [
    path("add-fees/<int:pkid>/<str:matricule>/", views.add_fee_view, name="add-fee"),
    path(
        "add-extra-payments/<int:pkid>/<str:matricule>/",
        views.add_extra_payments,
        name="add-extras",
    ),
    path("edit-fees/<int:pkid>/<str:matricule>/", views.edit_fee_view, name="edit-fee"),
]

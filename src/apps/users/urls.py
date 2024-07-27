from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above


app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="user-login"),
    path("logout/", views.logout_view, name="user-logout"),
    path(
        "reset-password",
        PasswordResetView.as_view(success_url="password-reset-done"),
        name="reset_password",
    ),
    path(
        "password-reset-done",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

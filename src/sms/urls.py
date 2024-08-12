from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import include, path

from apps.scelery.views import form_view
from apps.teachers import views
from apps.students.views import get_classes_by_department

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    # local apps
    path("", include("apps.staff.urls", namespace="staff")),
    path("students/", include("apps.students.urls", namespace="students")),
    path("teachers/", include("apps.teachers.urls", namespace="teachers")),
    path("payments/", include("apps.fees.urls", namespace="fees")),
    path("settings/", include("apps.settings.urls", namespace="settings")),
    path("sessions/", include("apps.terms.urls", namespace="sessions")),
    path("reports/", include("apps.reports.urls", namespace="reports")),
    # Classes
    path("classes/", views.class_list_view, name="class-list"),
    path("add-class/", views.class_add_view, name="class-add"),
    path("edit/<int:pkid>/", views.class_edit_view, name="class-edit"),
    path("delete/<int:pkid>/", views.class_delete_view, name="class-delete"),
    path(
        "download-sample-class-upload/",
        views.download_sample_class_file,
        name="download-sample-class-upload",
    ),
    path(
        "upload-class-from-file",
        views.upload_classes_from_file,
        name="upload-class-from-file",
    ),
    # auth
    path("accounts/", include("apps.users.urls", namespace="users")),
    path(
        "password-reset-complete",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("attendance/", include("apps.attendance.urls", namespace="attendance")),
    path("leave/", include("apps.leave.urls", namespace="leave")),
    # testing
    path("form/", form_view, name="form"),
    path(
        "get-classes/",
        get_classes_by_department,
        name="get_classes_by_department",
    ),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

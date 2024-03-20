from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.teachers import views


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

    # Classes
    path("classes/", views.class_list_view, name="class-list"),
    path("add-class/", views.class_add_view, name="class-add"),
    path("edit/<int:pkid>/", views.class_edit_view, name="class-edit"),
    path("delete/<int:pkid>/", views.class_delete_view, name="class-delete"),

    # auth
    path('accounts/', include('apps.users.urls', namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

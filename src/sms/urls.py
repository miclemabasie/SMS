from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),

    # local apps
    path("", include("apps.staff.urls", namespace="staff")),
    path("students/", include("apps.students.urls", namespace="students")),
    path("teachers/", include("apps.teachers.urls", namespace="teachers"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

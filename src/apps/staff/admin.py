from django.contrib import admin

from apps.students.models import Subject

from .models import AdminProfile


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ["pkid", "user", "gender", "phone_number", "country"]
    list_filter = ["gender", "country"]
    list_display_links = ["pkid", "user"]


admin.site.register(AdminProfile, AdminProfileAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ["pkid", "name", "code", "description"]
    list_display_links = ["pkid", "name", "code"]


admin.site.register(Subject, SubjectAdmin)

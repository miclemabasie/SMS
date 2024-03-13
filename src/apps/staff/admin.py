from django.contrib import admin
from .models import AdminProfile
from apps.students.models import Subject


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "gender", "phone_number", "country"]
    list_filter = ["gender", "country"]
    list_display_links = ["id", "pkid", "user"]


admin.site.register(AdminProfile, AdminProfileAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ["pkid", "name", "code", "description"]
    list_display_links = ["pkid", "name", "code"]


admin.site.register(Subject, SubjectAdmin)
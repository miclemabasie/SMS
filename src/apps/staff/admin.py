from django.contrib import admin
from .models import AdminProfile


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "gender", "phone_number", "country"]
    list_filter = ["gender", "country"]
    list_display_links = ["id", "pkid", "user"]


admin.site.register(AdminProfile, AdminProfileAdmin)

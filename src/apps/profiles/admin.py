from django.contrib import admin
from .models import ParentProfile


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ["id", "pkid", "user", "gender", "phone_number", "country", "city"]
#     list_filter = ["gender", "country", "city"]
#     list_display_links = ["id", "pkid", "user"]


# admin.site.register(Profile, ProfileAdmin)

class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ["full_name", "address", "email", "role"]


admin.site.register(ParentProfile, ParentProfileAdmin)
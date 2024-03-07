from django.contrib import admin
from .models import ReportCard

class ReportCardAdmin(admin.ModelAdmin):
    list_display = ["student", "session", "generated_by"]


admin.site.register(ReportCard, ReportCardAdmin)

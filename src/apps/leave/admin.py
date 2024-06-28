from django.contrib import admin
from .models import TeacherLeave, AdminLeave, StudentLeave

# Register your models here.


class TeacherLeaveAdmin(admin.ModelAdmin):
    list_display = ["teacher", "reason", "leave_date", "duration", "submitted_on"]


class AdminLeaveAdmin(admin.ModelAdmin):
    list_display = ["admin", "reason", "leave_date", "duration", "submitted_on"]


class StudentLeaveAdmin(admin.ModelAdmin):
    list_display = ["student", "reason", "leave_date", "duration", "submitted_on"]


admin.site.register(TeacherLeave, TeacherLeaveAdmin)
admin.site.register(AdminLeave, AdminLeaveAdmin)
admin.site.register(StudentLeave, StudentLeaveAdmin)

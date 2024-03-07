from django.contrib import admin
from .models import StudentProfile, Subject, Mark, Class

class MarkAdmin(admin.TabularInline):
    model = Mark
    fk_name = "student"
    extra = 5
    fields = ["score", "teacher", "exam_session", "subject"]
    verbose_name = "Marks Associated to this student"
    can_delete = False


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "gender", "phone_number", "country", "is_repeater", "is_owing"]
    list_filter = ["gender", "country"]
    list_display_links = ["id", "pkid", "user"]

    inlines = [
        MarkAdmin
    ]


admin.site.register(StudentProfile, StudentProfileAdmin)


class SubjectAdmin(admin.TabularInline):
    model = Subject
    extra = 5
    fields = ["name", "description", "teachers"]

class ClassAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "class_name", "grade_level"]
    list_filter = ["grade_level"]
    list_display_links = ["id", "pkid", "class_name"]
    inlines = [
        SubjectAdmin
    ]

admin.site.register(Class, ClassAdmin)
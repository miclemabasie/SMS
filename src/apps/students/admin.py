from django.contrib import admin

from .models import Class, Mark, StudentProfile, Subject, TeacherProfile


class MarkAdmin(admin.TabularInline):
    model = Mark
    fk_name = "student"
    extra = 5
    fields = ["score", "teacher", "exam_session", "subject"]
    verbose_name = "Marks Associated to this student"
    can_delete = False


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["matricule", "pkid", "user", "gender", "phone_number", "country", "is_repeater", "is_owing"]
    list_filter = ["gender", "country"]
    list_display_links = ["matricule", "pkid", "user"]
    search_fields = ["matricule"]

    inlines = [
        MarkAdmin
    ]


admin.site.register(StudentProfile, StudentProfileAdmin)


class SubjectAdmin(admin.TabularInline):
    model = Subject
    extra = 5
    fields = ["name", "code" "description"]

class ClassAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "grade_level"]
    list_filter = ["grade_level"]
    list_display_links = ["id", "pkid"]
    

admin.site.register(Class, ClassAdmin)


class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "gender", "phone_number", "country"]
    list_filter = ["gender", "country"]
    list_display_links = ["id", "pkid", "user"]
    

admin.site.register(TeacherProfile, TeacherProfileAdmin)


"AIzaSyCl2wtzcjTd1ekKgpNNgQRNuqRjtM8qRic&libraries=places&callback=MapHandlers"
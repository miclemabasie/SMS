from django.contrib import admin
from .models import Term, AcademicYear, ExaminationSession


class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date"]

admin.site.register(AcademicYear, AcademicYearAdmin)

class TermAdmin(admin.ModelAdmin):
    list_display = ["academic_year", "term"]

admin.site.register(Term, TermAdmin)


class ExaminationSessionAdmin(admin.ModelAdmin):
    list_display = ["term", "exam_session"]

admin.site.register(ExaminationSession, ExaminationSessionAdmin)
from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.students.models import StudentProfile, Class
from apps.terms.models import Term, ExaminationSession
from apps.staff.models import AdminProfile
from django.utils.translation import gettext_lazy as _
from django.db.models import Max


class ReportCard(TimeStampedUUIDModel):
    student = models.ForeignKey(
        StudentProfile, related_name="report_card", on_delete=models.CASCADE
    )
    # klass = models.ForeignKey()
    session = models.ForeignKey(
        Term, related_name="report_cards", on_delete=models.CASCADE
    )
    generated_by = models.ForeignKey(
        AdminProfile, related_name="reports_generated", on_delete=models.CASCADE
    )
    remark = models.TextField(blank=True, null=True)


class AcademicRecord(TimeStampedUUIDModel):
    student = models.ForeignKey(
        StudentProfile, related_name="academic_record", on_delete=models.CASCADE
    )
    exam_term = models.ForeignKey(
        Term, related_name="record_report", on_delete=models.CASCADE
    )
    total_marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    student_rank = models.IntegerField(blank=True, null=True)
    term_avg = models.DecimalField(max_digits=5, decimal_places=2)
    klass = models.ForeignKey(
        Class, related_name="academic_records", on_delete=models.CASCADE
    )
    session_1_avg = models.DecimalField(max_digits=5, decimal_places=2)
    session_2_avg = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("student", "exam_term")

    def get_best_three_students(self):
        """
        Returns to get the first 3 students from a particular class based on the highest score in academic record
        """
        top_students = (
            AcademicRecord.objects.filter(klass=self.klass)
            .annotate(max_score=Max("total_marks_obtained"))
            .order_by("-max_score")[:3]
        )

        return top_students

    def get_last_three_students(self):
        """
        Returns to get the last 3 students from a particular class based on the lowest score in academic record
        """

        worst_students = (
            AcademicRecord.objects.filter(klass=self.klass)
            .annotate(max_score=Max("total_marks_obtained"))
            .order_by("-max_score")[-3:]
        )
        return worst_students

    def generate_class_master_report(self):
        data = {}
        data["class_master"] = self.klass.class_master
        data["best_students"] = self.get_best_three_students
        data["last_studenst"] = self.get_last_three_students
        data["class_master_report"] = "Some logic to be implemented"

        return data

from django.db import models
from django.db.models import Max, Q
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel
from apps.staff.models import AdminProfile
from apps.students.models import Class, StudentProfile
from apps.terms.models import ExaminationSession, Term


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

    @staticmethod
    def get_best_three_students(class_, term):
        """
        Returns to get the first 3 students from a particular class based on the highest score in academic record
        """
        top_students = (
            AcademicRecord.objects.filter(klass=class_, exam_term=term)
            .annotate(max_score=Max("total_marks_obtained"))
            .order_by("-max_score")[:3]
        )

        return top_students

    @staticmethod
    def get_last_three_students(class_, term):
        """
        Returns to get the last 3 students from a particular class based on the lowest score in academic record
        """

        worst_students = (
            AcademicRecord.objects.filter(klass=class_, exam_term=term)
            .annotate(max_score=Max("total_marks_obtained"))
            .order_by("max_score")[:3]
        )
        return worst_students

    @staticmethod
    def get_number_passed_in_a_term(term, class_, pass_avg):
        # get all records for this class that patten to this term
        acadmic_records = AcademicRecord.objects.filter(
            klass=class_, exam_term=term, term_avg__gte=pass_avg
        )
        if acadmic_records.exists():
            # students passed in this term
            # get students with term avg > 10
            return acadmic_records
        else:
            return None

    @staticmethod
    def get_highest_student_in_a_term(term, class_, pass_avg=None):
        if pass_avg is None:
            pass_avg = class_.pass_avg
        # Get the student with the highest avg for a given class in a particular term
        acadmic_records = AcademicRecord.objects.filter(
            exam_term=term, klass=class_
        ).order_by("-term_avg")
        if acadmic_records.exists():
            # get the first student in the queryset
            return acadmic_records.first()
        else:
            return None

    @staticmethod
    def get_lowest_student_in_a_term(term, class_, pass_avg=None):
        if pass_avg is None:
            pass_avg = class_.pass_avg
        # Get the student with the lowest avg for a given class in a particular term
        acadmic_records = AcademicRecord.objects.filter(
            exam_term=term, klass=class_
        ).order_by("-term_avg")
        if acadmic_records.exists():
            # get the first student in the queryset
            return acadmic_records.last()
        else:
            return None

    # @staticmethod
    # def get_number_failed_in_a_term(term, class_, pass_avg):
    #     # get all records for this class that patten to this term
    #     acadmic_records = AcademicRecord.objects.filter(
    #         klass=class_, exam_term=term, term_avg__lt=pass_avg
    #     )
    #     if acadmic_records.exists():
    #         # students passed in this term
    #         # get students with term avg > 10
    #         return acadmic_records
    #     else:
    #         return None

    @staticmethod
    def perform_grading(term, class_, lower_bound, upper_bound):

        students = AcademicRecord.objects.filter(
            Q(term_avg__gte=lower_bound) & Q(term_avg__lte=upper_bound),
            klass=class_,
            exam_term=term,
        )
        return students


class ReportGenerationStatus(models.Model):
    task_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    file_path = models.TextField(null=True, blank=True)
    file_name = models.CharField(max_length=256, blank=True, null=True)
    klass = models.ForeignKey(
        Class,
        related_name="renerated_reports",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Add file path during saving
    def save(self, *args, **kwargs):
        print(self.file_path)
        if self.file_path:
            # set file name
            self.file_name = self.file_path[(self.file_path.index("/") + 1) :]
        return super().save(*args, **kwargs)

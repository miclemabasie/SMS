from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.students.models import StudentProfile
from apps.terms.models import Term, ExaminationSession

from apps.staff.models import AdminProfile
from django.utils.translation import gettext_lazy as _


class ReportCard(TimeStampedUUIDModel):
    student = models.ForeignKey(StudentProfile, related_name="report_card", on_delete=models.CASCADE)
    # klass = models.ForeignKey()
    session = models.ForeignKey(Term, related_name="report_cards", on_delete=models.CASCADE)
    generated_by = models.ForeignKey(AdminProfile, related_name="reports_generated", on_delete=models.CASCADE)
    remark = models.TextField(blank=True, null=True)
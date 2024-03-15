from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.staff.models import AdminProfile
from django.utils.translation import gettext_lazy as _
from apps.students.models import StudentProfile


class FeeTypeChoice(models.TextChoices):
    PTA = "pta", _("PTA Fee")
    SCHOOL_FEES = "school_fees", _("School Fees")
    OTHER = "other", _("Other")


class Fee(TimeStampedUUIDModel):
    amount = models.PositiveIntegerField()
    fee_type = models.CharField(
        verbose_name = _('Session'),
        max_length=20,
        choices=FeeTypeChoice.choices,
        default=FeeTypeChoice.SCHOOL_FEES,
    )
    target = models.PositiveIntegerField()
    is_complete = models.BooleanField(default=False)
    student = models.ForeignKey(StudentProfile, related_name="fees", on_delete=models.CASCADE)
    recieved_by = models.ForeignKey(AdminProfile, related_name="collected_fees", on_delete=models.SET_NULL, blank=True, null=True)


    def save(self, *args, **kwargs):
        if self.amount == self.target:
            self.is_complete = True
        return super().save(*args, **kwargs)

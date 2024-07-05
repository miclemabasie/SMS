from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.staff.models import AdminProfile
from apps.terms.models import AcademicYear
from django.utils.translation import gettext_lazy as _
from apps.students.models import StudentProfile, Class
from django.utils import timezone
from apps.settings.models import Setting


class FeeTypeChoice(models.TextChoices):
    PTA = "pta", _("PTA Fee")
    SCHOOL_FEES = "school_fees", _("School Fees")
    OTHER = "other", _("Other")


class Fee(TimeStampedUUIDModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_type = models.CharField(
        verbose_name=_("Fee Type"),
        max_length=20,
        choices=FeeTypeChoice.choices,
        default=FeeTypeChoice.SCHOOL_FEES,
    )
    target = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    student = models.ForeignKey(
        StudentProfile, related_name="fees", on_delete=models.CASCADE
    )
    recieved_by = models.ForeignKey(
        AdminProfile,
        related_name="collected_fees",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        related_name="fees_paid",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    # Modified
    date_of_payment = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        print("the save methos is called")
        setting = Setting.objects.all().first()
        if self.amount >= setting.get_complete_fee:
            self.is_complete = True
        else:
            self.is_complete = False
        return super().save(*args, **kwargs)


class FeePaymentHistory(TimeStampedUUIDModel):
    fee = models.ForeignKey(Fee, related_name="fee_history", on_delete=models.CASCADE)
    student = models.ForeignKey(
        StudentProfile, related_name="payment_history", on_delete=models.CASCADE
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    collected_by = models.ForeignKey(
        AdminProfile, on_delete=models.SET_NULL, blank=True, null=True
    )
    pay_date = models.DateTimeField(default=timezone.now)
    fee_type = models.CharField(
        verbose_name=_("FeeType"), max_length=20, blank=True, null=True
    )


class ExtraPayment(TimeStampedUUIDModel):
    name = models.CharField(max_length=200)
    remark = models.TextField()
    student = models.ForeignKey(
        StudentProfile, related_name="extra_payments", on_delete=models.CASCADE
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    collected_by = models.ForeignKey(
        AdminProfile, on_delete=models.SET_NULL, blank=True, null=True
    )
    pay_date = models.DateTimeField(default=timezone.now)

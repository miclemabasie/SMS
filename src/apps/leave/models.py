from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel
from apps.staff.models import AdminProfile
from apps.students.models import StudentProfile, TeacherProfile

# Create your models here.


class LEAVESTATUSCHOICES(models.TextChoices):
    PENDING = "Pending", _("Pending")
    APPROVED = "Approved", _("Approved")
    REJECTED = "Rejected", _("Rejected")


class LEAVEAPPROVALSTATUS(models.TextChoices):
    PENDING = "Pending", _("Pending")
    APPROVED = "Approved", _("Approved")
    REJECTED = "Rejected", _("Rejected")


class TeacherLeave(TimeStampedUUIDModel):
    teacher = models.ForeignKey(
        TeacherProfile, related_name="teacher_leaves", on_delete=models.DO_NOTHING
    )
    reason = models.TextField()
    approval_status = models.CharField(
        max_length=30,
        choices=LEAVEAPPROVALSTATUS.choices,
        default=LEAVEAPPROVALSTATUS.PENDING,
    )
    leave_date = models.DateField()
    duration = models.CharField(max_length=20)
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=LEAVESTATUSCHOICES.choices,
        default=LEAVESTATUSCHOICES.PENDING,
    )

    def __str__(self):
        return f"Leave-{self.teacher.user.username}"


class AdminLeave(TimeStampedUUIDModel):
    admin = models.ForeignKey(
        AdminProfile, related_name="teacher_leaves", on_delete=models.DO_NOTHING
    )
    reason = models.TextField()
    approval_status = models.CharField(
        max_length=30,
        choices=LEAVEAPPROVALSTATUS.choices,
        default=LEAVEAPPROVALSTATUS.PENDING,
    )
    leave_date = models.DateField()
    duration = models.CharField(max_length=20)
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=LEAVESTATUSCHOICES.choices,
        default=LEAVESTATUSCHOICES.PENDING,
    )

    def __str__(self):
        return f"Leave-{self.admin.user.username}"


class StudentLeave(TimeStampedUUIDModel):
    student = models.ForeignKey(
        StudentProfile, related_name="teacher_leaves", on_delete=models.DO_NOTHING
    )
    reason = models.TextField()
    approval_status = models.CharField(
        max_length=30,
        choices=LEAVEAPPROVALSTATUS.choices,
        default=LEAVEAPPROVALSTATUS.PENDING,
    )
    leave_date = models.DateField()
    duration = models.CharField(max_length=20)
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=LEAVESTATUSCHOICES.choices,
        default=LEAVESTATUSCHOICES.PENDING,
    )

    def __str__(self):
        return f"Leave-{self.student.user.username}"

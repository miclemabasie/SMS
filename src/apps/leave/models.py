from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.students.models import TeacherProfile, StudentProfile
from apps.staff.models import AdminProfile
from django.utils.translation import gettext_lazy as _

# Create your models here.


class LEAVESTATUSCHOICES(models.TextChoices):
    PENDING = "Pending", _("Pending")
    APPROVED = "Approved", _("Approved")
    REJECTED = "Rejected", _("Rejected")
    EXPIRED = "Expired", _("Expired")


class TeacherLeave(TimeStampedUUIDModel):
    teacher = models.ForeignKey(
        TeacherProfile, related_name="teacher_leaves", on_delete=models.DO_NOTHING
    )
    reason = models.TextField()
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

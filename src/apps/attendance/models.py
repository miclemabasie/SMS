from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.staff.models import AdminProfile
from apps.students.models import StudentProfile, Subject, TeacherProfile
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Attendance(TimeStampedUUIDModel):
    is_present = models.BooleanField(default=False)
    student = models.ForeignKey(
        StudentProfile, related_name="attendance", on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        TeacherProfile, related_name="student_attendance", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="attendance", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class DailyAttendance(TimeStampedUUIDModel):
    user = models.ForeignKey(
        User, related_name="daily_attendance", on_delete=models.CASCADE
    )
    taken_by = models.ForeignKey(
        AdminProfile,
        related_name="daily_attendance",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    day = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=False)

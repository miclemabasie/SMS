from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.students.models import StudentProfile, Subject, TeacherProfile


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

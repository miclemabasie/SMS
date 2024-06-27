from django.db import models
from apps.common.models import TimeStampedUUIDModel
from apps.students.models import TeacherProfile, StudentProfile
from apps.staff.models import AdminProfile

# Create your models here.


class TeacherLeave(TimeStampedUUIDModel):
    staff = models.ForeignKey(
        TeacherProfile, related_name="teacher_leaves", on_delete=models.DO_NOTHING
    )
    reason = models.TextField()
    leave_date = models.DateField()
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leave-{self.staff.user.username}"

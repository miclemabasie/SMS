from django.db import models
from apps.students.models import StudentProfile, TeacherProfile
from apps.staff.models import AdminProfile
from apps.common.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(TimeStampedUUIDModel):
    name = models.CharField(max_length=255, verbose_name="Announcement Category")
    description = models.TextField(
        verbose_name="Announcement Description", help_text="Description of announcement"
    )

    def __str__(self):
        return self.name


class PRIORITY_CHOICES(models.TextChoices):
    HIGH = "High", _("High")
    MEDIUM = "Medium", _("Medium")
    LOW = "Low", _("Low")


class Announcement(TimeStampedUUIDModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    priority = models.CharField(
        max_length=6, choices=PRIORITY_CHOICES, default=PRIORITY_CHOICES.MEDIUM
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    visible_to_students = models.BooleanField(default=False)
    visible_to_parents = models.BooleanField(default=False)
    visible_to_teachers = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title.title()} - {self.category.name.title()}"


class Attachment(models.Model):
    announcement = models.ForeignKey(
        Announcement, related_name="attachments", on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="attachments/%Y/%m/%d/")
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.file.name


class Event(TimeStampedUUIDModel):
    name = models.CharField(max_length=255, verbose_name=_("Event Name"))
    description = models.TextField(verbose_name=_("Event Description"))
    date = models.DateField(verbose_name=_("Event Date"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    visible_to_students = models.BooleanField(default=False)
    visible_to_parents = models.BooleanField(default=False)
    visible_to_teachers = models.BooleanField(default=True)
    location = models.CharField(
        max_length=255, verbose_name=_("Event Location"), blank=True, null=True
    )

    def __str__(self):
        return self.name.title()

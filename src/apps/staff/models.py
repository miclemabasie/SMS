from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import BooleanField
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedUUIDModel
from apps.common.utils import auto_create_matricule
from apps.profiles.models import Gender
from apps.students.models import Subject

User = get_user_model()


class Role(models.TextChoices):
    PRINCIPAL = "Principal", _("Principal")
    VICE_PRINCIPAL = "Vice Principal", _("Vice Principal")
    BURSER = "Burser", _("Burser")
    IT = "IT", _("IT")
    DM = "DM", _("DM")
    SECRETARY = "Secretary", _("Secretary")
    OTHER = "Other", _("Other")


class AdminProfile(TimeStampedUUIDModel):
    user = models.OneToOneField(
        User, related_name="admin_profile", on_delete=models.CASCADE
    )
    number_of_absences = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    subjects = models.ManyToManyField(Subject)
    remark = models.TextField(verbose_name=_("Remark"), blank=True, null=True)
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=200,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+237680672888"
    )
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/profile_default.png"
    )
    country = models.CharField(
        verbose_name=_("Country"), max_length=200, default="CM", blank=False, null=False
    )
    location = models.CharField(
        verbose_name=_("Location"), max_length=100, blank=True, null=True
    )
    address = models.CharField(verbose_name=_("Address"), max_length=200)
    responsibilities = models.TextField(
        verbose_name=_("Responsibility"), blank=True, null=True
    )
    can_manage = models.CharField(max_length=100)

    is_admin = models.BooleanField(default=True)

    matricule = models.CharField(blank=True, null=True, max_length=200, unique=True)
    role = models.CharField(
        verbose_name=_("Role"),
        choices=Role.choices,
        default=Role.OTHER,
        max_length=200,
    )

    generate_reports = models.BooleanField(
        verbose_name=_("Generate Reports"), default=False
    )
    manage_students = models.BooleanField(
        verbose_name=_("Manage Students"), default=False
    )
    manage_teachers = models.BooleanField(
        verbose_name=_("Manage Teachers"), default=False
    )
    manage_admins = models.BooleanField(
        verbose_name=_("Manage Administrators"), default=False
    )
    manage_sessions = models.BooleanField(
        verbose_name=_("Manage Sessions"), default=False
    )
    manage_subjects = models.BooleanField(
        verbose_name=_("Manage Subjects"), default=False
    )

    is_teacher = models.BooleanField(verbose_name=_("Is Teacher"), default=False)

    def save(self, *args, **kwargs):
        self.matricule = auto_create_matricule("staff")
        return super().save(*args, **kwargs)

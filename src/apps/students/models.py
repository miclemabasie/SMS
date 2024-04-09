import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel
from apps.profiles.models import Gender, ParentProfile
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel

# from apps.teachers.models import TeacherProfile
from apps.terms.models import ExaminationSession

from apps.common.utils import auto_create_matricule


class DOMAINCHOICES(models.TextChoices):
    ARTS = "Arts", _("Arts")
    SCIENCE = "Science", _("Science")
    COMMERCIAL = "Commercial", _("Commercial")
    INSDUSTRIAL = "Industrial", _("Industrial")
    OTHER = "Other", _("Other")


User = get_user_model()


class Class(TimeStampedUUIDModel):
    class_name = models.CharField(verbose_name=_("Class Name"), max_length=200)
    grade_level = models.CharField(verbose_name=_("Class Level"), max_length=200)
    class_master = models.CharField(
        verbose_name=_("Class Master"), max_length=200, blank=True, null=True
    )
    class_prefect = models.CharField(
        verbose_name=_("Class Prefect"), max_length=200, blank=True, null=True
    )
    subjects = models.ManyToManyField("Subject", related_name="subjects", blank=True)


class StudentProfile(TimeStampedUUIDModel):
    user = models.OneToOneField(
        User, related_name="student_profile", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        ParentProfile,
        related_name="childrend",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    current_class = models.ForeignKey(
        "Class",
        on_delete=models.SET_NULL,
        related_name="students",
        blank=True,
        null=True,
    )
    number_of_absences = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    remark = models.TextField(verbose_name=_("Remark"), blank=True, null=True)
    is_repeater = models.BooleanField(default=False)
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+237670000000"
    )
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"),
        default="/profile_default.png",
        upload_to="student_profile_photos/",
    )
    country = CountryField(
        verbose_name=_("Country"), default="CM", blank=False, null=False
    )
    address = models.CharField(verbose_name=_("Address"), max_length=200)
    is_owing = models.BooleanField(default=True)
    is_student = models.BooleanField(default=True)
    matricule = models.CharField(blank=True, null=True, max_length=200, unique=True)
    domain = models.CharField(
        verbose_name=_("Domain"),
        choices=DOMAINCHOICES.choices,
        default=DOMAINCHOICES.OTHER,
        max_length=20,
    )

    # Adding optional subjects for the student
    optional_subjects = models.ManyToManyField(
        "Subject", related_name="students_taking"
    )

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = auto_create_matricule("student")
        return super().save(*args, **kwargs)


class Attendance(TimeStampedUUIDModel):
    is_present = models.BooleanField(default=False)
    student = models.ForeignKey(
        StudentProfile, related_name="attendance", on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(
        "TeacherProfile", related_name="student_attendance", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        "Subject", related_name="attendance", on_delete=models.CASCADE
    )


class Subject(TimeStampedUUIDModel):
    # klass = models.ForeignKey(Class, related_name="subjects", on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("Subject Name"), max_length=200)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(
        verbose_name=_("Subject Code"), max_length=10, blank=True, null=True
    )
    coef = models.PositiveIntegerField(verbose_name=_("Subject Code"), default=1)

    # Add a ManyToManyField for teachers
    # teachers = models.ManyToManyField("TeacherProfile", related_name="subjects_taught", blank=True)

    def __str__(self):
        return f"{self.name}-{self.code}"


class Mark(TimeStampedUUIDModel):
    score = models.IntegerField(default=0)
    student = models.ForeignKey(
        StudentProfile,
        related_name="student_marks",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    teacher = models.ForeignKey(
        "TeacherProfile",
        related_name="marks",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    exam_session = models.ForeignKey(
        ExaminationSession, related_name="session_marks", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="subject_marks", on_delete=models.CASCADE
    )
    remark = models.CharField(
        max_length=255, verbose_name=_("Remark"), blank=True, null=True
    )


class TeacherProfile(TimeStampedUUIDModel):
    user = models.OneToOneField(
        User, related_name="teacher_profile", on_delete=models.CASCADE
    )
    number_of_absences = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(9), MaxValueValidator(1)]
    )
    subjects = models.ManyToManyField("Subject", related_name="teacher")
    remark = models.TextField(verbose_name=_("Remark"), blank=True, null=True)

    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+237680672888"
    )
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/profile_default.png"
    )
    country = CountryField(
        verbose_name=_("Country"), default="CM", blank=False, null=False
    )
    location = models.CharField(
        verbose_name=_("Location"), max_length=100, blank=True, null=True
    )
    address = models.CharField(verbose_name=_("Address"), max_length=200)
    matricule = models.CharField(blank=True, null=True, max_length=200, unique=True)
    main_subject = models.CharField(
        verbose_name=_("Main Subject"), blank=True, null=True, max_length=200
    )

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = auto_create_matricule("staff")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_fullname}"

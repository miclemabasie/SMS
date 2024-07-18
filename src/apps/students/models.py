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
from django.db.models import Sum, Count
from apps.settings.models import Setting
from apps.terms.models import AcademicYear, Term

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
    # subjects = models.ManyToManyField("Subject", related_name="classes", blank=True)
    pass_avg = models.IntegerField(default=10)

    best_subject = models.CharField(max_length=255, blank=True, null=True)
    worst_subject = models.CharField(max_length=255, blank=True, null=True)

    def get_full_name(self):
        return f"{self.grade_level}-{self.class_name}"

    def get_total_girls(self):
        total_female_students_qs = self.students.filter(gender="Female").aggregate(
            total_female_students=Count("id")
        )
        return total_female_students_qs["total_female_students"]

    def get_total_boys(self):
        total_male_students_qs = self.students.filter(gender="Male").aggregate(
            total_male_students=Count("id")
        )
        return total_male_students_qs["total_male_students"]

    def get_total_enrol(self):
        return self.get_total_boys() + self.get_total_girls()

    @property
    def get_total_template_enrol(self):
        return self.get_total_enrol()

    @property
    def get_class_name(self):
        return f"{self.grade_level}-{self.class_name}"


class ClassAcademicRecord(TimeStampedUUIDModel):
    klass = models.ForeignKey(Class, related_name="records", on_delete=models.CASCADE)
    term = models.ForeignKey(
        Term, related_name="classes_academic_records", on_delete=models.CASCADE
    )
    class_avg = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("klass", "term")

    @staticmethod
    def get_class_avg(term, klass):
        records = ClassAcademicRecord.objects.filter(term=term, klass=klass)
        print("this are the records", records)
        if records:
            print("this are the records")
            return records.first().class_avg
        else:
            return None


# used to hold students's information until they change their password after they are being created,
# Then this record is deleted
class StudentTempCreateProfile(models.Model):
    pin = models.CharField(max_length=10, verbose_name=_("PIN"))
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    student = models.OneToOneField(
        "StudentProfile",
        verbose_name=_("Student"),
        on_delete=models.SET_NULL,
        null=True,
    )


# used to hold teacher's information until they change their password after they are being created,
# Then this record is deleted
class TeacherTempCreateProfile(models.Model):
    pin = models.CharField(max_length=10, verbose_name=_("PIN"))
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    teacher = models.OneToOneField(
        "TeacherProfile",
        verbose_name=_("Student"),
        on_delete=models.SET_NULL,
        null=True,
    )


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
    has_paid_pta = models.BooleanField(default=False)
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
    specialty = models.CharField(max_length=200, default="Civil Engineering")
    is_activated = models.BooleanField(default=True)

    # Adding optional subjects for the student
    optional_subjects = models.ManyToManyField(
        "Subject", related_name="students_taking"
    )

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = auto_create_matricule("student")
        return super().save(*args, **kwargs)

    def get_all_subjects(self):
        # get all the subjects associated to the student
        # Get all the subjects in the class the student belongs to
        # and those optionally added by the student
        subjects1 = self.current_class.subjects.all()
        # get optoinal subjects for the particular student
        optional_subjects = self.optional_subjects.all()

        distinct_subjects = set(list(subjects1) + list(optional_subjects))

        return list(distinct_subjects)

    def get_sum_of_subjects_coef(self):
        subjects = self.get_all_subjects()
        total_coef = sum([s.coef for s in subjects])
        return total_coef

    def get_payment_history_for_current_year(self):
        current_year = AcademicYear.objects.get(is_current=True)
        return self.payment_history.filter(
            fee__fee_type="school_fees", fee__academic_year=current_year
        )

    def get_amount_paid(self):
        total_fees = 0
        payment_records = self.get_payment_history_for_current_year()
        for pay in payment_records:
            total_fees += pay.amount_paid
        return total_fees

    @property
    def get_student_is_owing(self):
        setting = Setting.objects.all().first()
        if self.get_amount_paid() == setting.get_complete_fee:
            return True
        return False

    @property
    def has_paid_only_first(self):
        setting = Setting.objects.all().first()
        if self.get_amount_paid() == setting.first_installment:
            return True

    @property
    def get_total_extra_amount(self):
        extras = self.extra_payments.all()
        total = 0
        for payment in extras:
            total += payment.amount_paid
        return total


# class Attendance(TimeStampedUUIDModel):
#     is_present = models.BooleanField(default=False)
#     student = models.ForeignKey(
#         StudentProfile, related_name="attendance", on_delete=models.CASCADE
#     )
#     teacher = models.ForeignKey(
#         "TeacherProfile", related_name="student_attendance", on_delete=models.CASCADE
#     )
#     subject = models.ForeignKey(
#         "Subject", related_name="attendance", on_delete=models.CASCADE
#     )
#     created_at = models.DateTimeField(auto_now_add=True)


class Subject(TimeStampedUUIDModel):
    # klass = models.ForeignKey(Class, related_name="subjects", on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_("Subject Name"), max_length=200)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(
        verbose_name=_("Subject Code"), max_length=10, blank=True, null=True
    )
    klass = models.ForeignKey(
        Class, related_name="subjects", on_delete=models.SET_NULL, blank=True, null=True
    )

    has_class = models.BooleanField(default=False)
    coef = models.PositiveIntegerField(verbose_name=_("Subject Coef"), default=1)

    assigned_to = models.ForeignKey(
        "TeacherProfile",
        related_name="assigned_subjects",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    assigned = models.BooleanField(default=False)

    # Add a ManyToManyField for teachers
    # teachers = models.ManyToManyField("TeacherProfile", related_name="subjects_taught", blank=True)

    def __str__(self):
        return f"{self.code}-{self.name}"


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


class TEACHERSERVICE(models.TextChoices):
    CENTRAL = "Central", _("Central")
    DECONCENTRATED = "Deconcentrated", _("Deconcentrated")
    ATTACHED = "Attached", _("Attached")
    EXTERNAL = "External", _("External")
    OTHER = "Other", _("Other")


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

    # extras
    region_of_origin = models.CharField(
        verbose_name=_("Region of Origin"), max_length=200, blank=True, null=True
    )
    division_of_origin = models.CharField(
        verbose_name=_("Division of Origin"), max_length=200, blank=True, null=True
    )
    sub_division_of_origin = models.CharField(
        verbose_name=_("Sub Division of Origin"), max_length=200, blank=True, null=True
    )
    date_recruitement_public_service = models.CharField(
        verbose_name=_("Date of Recruitement into Public Service"),
        max_length=200,
        blank=True,
        null=True,
    )
    corps = models.CharField(
        verbose_name=_("Corps"), max_length=200, blank=True, null=True
    )
    career_grade = models.CharField(
        verbose_name=_("Career Grade"), max_length=200, blank=True, null=True
    )
    payroll_grade = models.CharField(
        verbose_name=_("Payroll Grade"), max_length=200, blank=True, null=True
    )
    career_category = models.CharField(
        verbose_name=_("Career Category"), max_length=200, blank=True, null=True
    )
    payroll_category_solde = models.CharField(
        verbose_name=_("Payroll Category Solde"), max_length=200, blank=True, null=True
    )
    career_index = models.CharField(
        verbose_name=_("Career Index"), max_length=200, blank=True, null=True
    )
    payroll_index = models.CharField(
        verbose_name=_("Payroll Index"), max_length=200, blank=True, null=True
    )
    career_echelon = models.CharField(
        verbose_name=_("Career Echelon"), max_length=200, blank=True, null=True
    )
    payroll_echelon = models.CharField(
        verbose_name=_("Payroll Echelon"), max_length=200, blank=True, null=True
    )
    service = models.CharField(
        verbose_name=_("Service"),
        choices=TEACHERSERVICE.choices,
        default=TEACHERSERVICE.OTHER,
        max_length=20,
        blank=True,
        null=True,
    )
    appointed_structure = models.CharField(
        verbose_name=_("Appointed Structure"), max_length=200, blank=True, null=True
    )
    town = models.CharField(
        verbose_name=_("Town"), max_length=200, blank=True, null=True
    )
    possition_rank = models.CharField(
        verbose_name=_("Position Rank"), max_length=200, blank=True, null=True
    )
    longivity_of_post = models.CharField(
        verbose_name=_("Longivity of Post"),
        help_text=_("Longivity of post in years"),
        max_length=200,
        blank=True,
        null=True,
    )
    longivity_in_administration = models.CharField(
        verbose_name=_("Longivity in Administration"),
        max_length=200,
        blank=True,
        null=True,
    )
    appointment_decision_reference = models.CharField(
        verbose_name=_("Reference of the Appointment Decision"),
        max_length=200,
        blank=True,
        null=True,
    )
    indemnity_situation = models.CharField(
        verbose_name=_("Indemnity Situation"), max_length=200, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = auto_create_matricule("staff")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_fullname}"

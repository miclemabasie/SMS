from django.db import models
from django.contrib.auth import get_user_model
from django.forms import BooleanField
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedUUIDModel
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.profiles.models import Gender
from apps.students.models import Subject

User = get_user_model()


class AdminProfile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name="admin_profile", on_delete=models.CASCADE)
    number_of_absences = models.PositiveIntegerField(default=0, validators=[MinValueValidator(9), MaxValueValidator(1)])
    subjects = models.ManyToManyField(Subject)
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
    location = models.CharField(verbose_name=_("Location"), max_length=100, blank=True, null=True)
    address = models.CharField(verbose_name=_("Address"), max_length=200)
    responsibilities = models.TextField(verbose_name=_("Responsibility"), blank=True, null=True)
    can_manage = models.CharField(max_length=100)




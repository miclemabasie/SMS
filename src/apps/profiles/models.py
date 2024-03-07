from django.db import models
from django.contrib.auth import get_user_model
from django.forms import BooleanField
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedUUIDModel
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


# class Profile(TimeStampedUUIDModel):
#     user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
#     phone_number = PhoneNumberField(
#         verbose_name=_("Phone Number"), max_length=30, default="+237680672888"
#     )
#     about_me = models.TextField(
#         verbose_name=_("About me"), default=_("Say something about yourself")
#     )
#     profile_photo = models.ImageField(
#         verbose_name=_("Profile Photo"), default="/profile_default.png"
#     )
#     gender = models.CharField(
#         verbose_name=_("Gender"),
#         choices=Gender.choices,
#         default=Gender.OTHER,
#         max_length=20,
#     )
#     country = CountryField(
#         verbose_name=_("Country"), default="CM", blank=False, null=False
#     )
#     # city = models.CharField(
#     #     verbose_name=_("City"),
#     #     max_length=180,
#     #     default="Bamenda",
#     #     blank=False,
#     #     null=False,
#     # )

#     def __str__(self):
#         return f"{self.user.username}'s profile"

class ParentProfile(TimeStampedUUIDModel):
    full_name = models.CharField(verbose_name=_("Full Name"), max_length=200)
    address = models.CharField(verbose_name=_("Address"), max_length=200)
    email = models.EmailField(verbose_name=_("Email"))
    role = models.CharField(verbose_name=_("Role"), max_length=50)

 
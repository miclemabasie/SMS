import uuid
from tabnanny import verbose

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(verbose_name=_("Username"), max_length=255)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=55)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=55)
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    dob = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

    def get_shortname(self):
        return self.username.title()

    @property
    def get_fullname(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_profile(self):
        # get the profile of user [admin, student or teacher]
        if self.is_admin:
            return self.admin_profile
        elif self.is_teacher:
            return self.teacher_profile
        elif self.is_student:
            return self.student_profile
        else:
            return ""

from wsgiref import validate
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valide email address"))

    def check_user_parameters(self, username, first_name, last_name, email):
        if not username:
            raise ValueError(_("User must provide username"))

        if not first_name:
            raise ValueError(_("User must provide First Name"))

        if not last_name:
            raise ValueError(_("User must provide a Last Name"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("BaseUser Account: An email address is required"))

    def create_user(
        self, username, first_name, last_name, email, password, **extra_fields
    ):

        self.check_user_parameters(username, first_name, last_name, email)

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, username, first_name, last_name, email, password, **extra_fields
    ):

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers must have is_superuser = True"))

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff = True"))

        if not password:
            raise ValueError(_("Superuser must provide a valid password"))

        self.check_user_parameters(username, first_name, last_name, email)

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

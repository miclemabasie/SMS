from django.db import models
from apps.common.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class Setting(TimeStampedUUIDModel):
    school_logo = models.FileField(
        verbose_name=_("Logo"), upload_to="settings", blank=True, null=True
    )
    school_favicon = models.FileField(
        verbose_name=_("Favicon"), upload_to="settings/", blank=True, null=True
    )
    school_name = models.CharField(
        verbose_name=_("School Name"), max_length=255, blank=True, null=True
    )
    currency = models.CharField(
        max_length=255,
        verbose_name=_("Currency"),
        help_text="Enter the currency you wish to appear on reciepts (CFA, XAF)",
        blank=True,
        null=True,
    )

    # School address information

    city = models.CharField(
        verbose_name=_("City"), max_length=255, blank=True, null=True
    )
    postal_code = models.CharField(
        verbose_name=_("Zip/Posttal Code"), max_length=255, blank=True, null=True
    )
    address1 = models.CharField(
        verbose_name=_("Address Line 1"), max_length=255, blank=True, null=True
    )
    address2 = models.CharField(
        verbose_name=_("Address Line 2"), max_length=255, blank=True, null=True
    )
    country = CountryField(
        verbose_name=_("Country"), default="CM", blank=False, null=False
    )

    motto = models.CharField(
        verbose_name=_("Motto"), max_length=255, blank=True, null=True
    )

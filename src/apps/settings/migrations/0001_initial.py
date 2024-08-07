# Generated by Django 5.0 on 2024-03-24 20:45

import uuid

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Setting",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "school_logo",
                    models.FileField(upload_to="settings", verbose_name="Logo"),
                ),
                (
                    "school_favicon",
                    models.FileField(upload_to="settings", verbose_name="Favicon"),
                ),
                (
                    "school_name",
                    models.CharField(max_length=255, verbose_name="School Name"),
                ),
                (
                    "currency",
                    models.CharField(
                        help_text="Enter the currency you wish to appear on reciepts (CFA, XAF)",
                        max_length=255,
                        verbose_name="Currency",
                    ),
                ),
                (
                    "address_line2",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Address Line 2",
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="City"
                    ),
                ),
                (
                    "postal_code",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Zip/Posttal Code",
                    ),
                ),
                (
                    "address_line1",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Address Line 1",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="CM", max_length=2, verbose_name="Country"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

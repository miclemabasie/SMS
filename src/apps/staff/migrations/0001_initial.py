# Generated by Django 5.0 on 2024-03-07 22:42

import django.core.validators
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("students", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminProfile",
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
                    "number_of_absences",
                    models.PositiveIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MinValueValidator(9),
                            django.core.validators.MaxValueValidator(1),
                        ],
                    ),
                ),
                (
                    "remark",
                    models.TextField(blank=True, null=True, verbose_name="Remark"),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Other", "Other"),
                        ],
                        default="Other",
                        max_length=20,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default="+237680672888",
                        max_length=30,
                        region=None,
                        verbose_name="Phone Number",
                    ),
                ),
                (
                    "profile_photo",
                    models.ImageField(
                        default="/profile_default.png",
                        upload_to="",
                        verbose_name="Profile Photo",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        default="CM", max_length=2, verbose_name="Country"
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Location"
                    ),
                ),
                ("address", models.CharField(max_length=200, verbose_name="Address")),
                (
                    "responsibilities",
                    models.TextField(
                        blank=True, null=True, verbose_name="Responsibility"
                    ),
                ),
                ("can_manage", models.CharField(max_length=100)),
                ("subjects", models.ManyToManyField(to="students.subject")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="admin_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

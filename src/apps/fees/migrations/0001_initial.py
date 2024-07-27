# Generated by Django 5.0 on 2024-03-07 22:42

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("staff", "0001_initial"),
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fee",
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
                ("amount", models.PositiveIntegerField()),
                (
                    "fee_type",
                    models.CharField(
                        choices=[
                            ("pta", "PTA Fee"),
                            ("school_fees", "School Fees"),
                            ("other", "Other"),
                        ],
                        default="school_fees",
                        max_length=20,
                        verbose_name="Session",
                    ),
                ),
                ("target", models.PositiveIntegerField()),
                ("is_complete", models.BooleanField(default=False)),
                (
                    "recieved_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="collected_fees",
                        to="staff.adminprofile",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fees",
                        to="students.studentprofile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

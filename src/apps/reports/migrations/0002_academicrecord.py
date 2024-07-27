# Generated by Django 5.0 on 2024-05-02 21:13

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0001_initial"),
        ("students", "0026_alter_subject_coef"),
        ("terms", "0010_alter_examinationsession_exam_session"),
    ]

    operations = [
        migrations.CreateModel(
            name="AcademicRecord",
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
                    "total_marks_obtained",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("student_rank", models.IntegerField(blank=True, null=True)),
                ("term_avg", models.DecimalField(decimal_places=2, max_digits=5)),
                ("session_1_avg", models.DecimalField(decimal_places=2, max_digits=5)),
                ("session_2_avg", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "exam_term",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="record_report",
                        to="terms.term",
                    ),
                ),
                (
                    "klass",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="academic_records",
                        to="students.class",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="record_report",
                        to="students.studentprofile",
                    ),
                ),
            ],
            options={
                "unique_together": {("student", "exam_term")},
            },
        ),
    ]

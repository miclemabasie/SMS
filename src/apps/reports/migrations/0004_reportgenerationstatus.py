# Generated by Django 5.0 on 2024-07-27 10:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0003_alter_academicrecord_student"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportGenerationStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task_id", models.CharField(max_length=255)),
                ("status", models.CharField(max_length=50)),
                ("file_path", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

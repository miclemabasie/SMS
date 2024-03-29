# Generated by Django 5.0 on 2024-03-10 11:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "students",
            "0004_studentprofile_is_student_studentprofile_matricule_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="studentprofile",
            name="domain",
            field=models.CharField(
                choices=[
                    ("Arts", "Arts"),
                    ("Science", "Science"),
                    ("Commercial", "Commercial"),
                    ("Industrial", "Industrial"),
                    ("Other", "Other"),
                ],
                default="Other",
                max_length=20,
                verbose_name="Domain",
            ),
        ),
    ]

# Generated by Django 5.0 on 2024-03-08 21:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="teachers",
            field=models.ManyToManyField(
                blank=True, related_name="subjects_taught", to="students.teacherprofile"
            ),
        ),
    ]

# Generated by Django 5.0 on 2024-07-05 13:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0043_rename_serivice_teacherprofile_service"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentprofile",
            name="has_paid_pta",
            field=models.BooleanField(default=False),
        ),
    ]

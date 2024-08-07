# Generated by Django 5.0 on 2024-08-07 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0048_studentprofile_pob"),
    ]

    operations = [
        migrations.AddField(
            model_name="class",
            name="class_code",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="studenttempcreateprofile",
            name="student",
            field=models.OneToOneField(
                default=42,
                on_delete=django.db.models.deletion.CASCADE,
                to="students.studentprofile",
                verbose_name="Student",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="teachertempcreateprofile",
            name="teacher",
            field=models.OneToOneField(
                default=16,
                on_delete=django.db.models.deletion.CASCADE,
                to="students.teacherprofile",
                verbose_name="Student",
            ),
            preserve_default=False,
        ),
    ]

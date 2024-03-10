# Generated by Django 5.0 on 2024-03-10 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0006_alter_studentprofile_number_of_absences"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mark",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="marks",
                to="students.teacherprofile",
            ),
        ),
    ]

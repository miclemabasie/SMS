# Generated by Django 5.0 on 2024-04-09 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0024_alter_studentprofile_remark"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mark",
            name="teacher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="marks",
                to="students.teacherprofile",
            ),
        ),
    ]
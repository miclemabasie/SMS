# Generated by Django 5.0 on 2024-07-27 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0004_reportgenerationstatus"),
        ("students", "0047_alter_classacademicrecord_class_avg"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportgenerationstatus",
            name="klass",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="renerated_reports",
                to="students.class",
            ),
        ),
    ]

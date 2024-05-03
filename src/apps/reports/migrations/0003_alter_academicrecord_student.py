# Generated by Django 5.0 on 2024-05-03 01:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0002_academicrecord"),
        ("students", "0026_alter_subject_coef"),
    ]

    operations = [
        migrations.AlterField(
            model_name="academicrecord",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="academic_record",
                to="students.studentprofile",
            ),
        ),
    ]

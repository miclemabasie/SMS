# Generated by Django 5.0 on 2024-06-26 10:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0037_alter_class_subjects"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teacherprofile",
            name="classes",
        ),
    ]
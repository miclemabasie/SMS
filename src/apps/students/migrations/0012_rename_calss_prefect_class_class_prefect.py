# Generated by Django 5.0 on 2024-03-12 13:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0011_class_calss_prefect_class_class_master"),
    ]

    operations = [
        migrations.RenameField(
            model_name="class",
            old_name="calss_prefect",
            new_name="class_prefect",
        ),
    ]

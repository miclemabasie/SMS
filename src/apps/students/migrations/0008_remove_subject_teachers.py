# Generated by Django 5.0 on 2024-03-10 15:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0007_alter_mark_teacher"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subject",
            name="teachers",
        ),
    ]
# Generated by Django 5.0 on 2024-07-14 21:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("settings", "0012_setting_next_opening_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="setting",
            name="teacher_can_upload",
            field=models.BooleanField(default=False),
        ),
    ]

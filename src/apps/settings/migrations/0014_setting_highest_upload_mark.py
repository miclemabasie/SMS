# Generated by Django 5.0 on 2024-08-11 22:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("settings", "0013_setting_teacher_can_upload"),
    ]

    operations = [
        migrations.AddField(
            model_name="setting",
            name="highest_upload_mark",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Highest Marks Allowed for upload"
            ),
        ),
    ]

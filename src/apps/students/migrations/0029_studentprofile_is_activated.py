# Generated by Django 5.0 on 2024-05-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0028_class_best_subject_class_worst_subject"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentprofile",
            name="is_activated",
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 5.0 on 2024-03-10 08:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_is_admin_alter_user_is_student_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="dob",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

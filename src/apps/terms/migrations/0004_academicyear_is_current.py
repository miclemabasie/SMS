# Generated by Django 5.0 on 2024-03-20 09:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("terms", "0003_alter_term_academic_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="academicyear",
            name="is_current",
            field=models.BooleanField(default=False),
        ),
    ]
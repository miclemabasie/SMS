# Generated by Django 5.0 on 2024-03-20 21:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("terms", "0008_examinationsession_is_current"),
    ]

    operations = [
        migrations.AlterField(
            model_name="examinationsession",
            name="is_current",
            field=models.BooleanField(default=False),
        ),
    ]

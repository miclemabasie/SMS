# Generated by Django 5.0 on 2024-08-12 01:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0051_alter_class_department"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentprofile",
            name="domain",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Arts", "Arts"),
                    ("Science", "Science"),
                    ("Commercial", "Commercial"),
                    ("Industrial", "Industrial"),
                    ("Other", "Other"),
                ],
                default="Other",
                max_length=20,
                null=True,
                verbose_name="Domain",
            ),
        ),
    ]
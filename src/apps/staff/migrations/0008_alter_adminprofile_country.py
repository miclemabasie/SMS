# Generated by Django 5.0 on 2024-07-05 23:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("staff", "0007_alter_adminprofile_number_of_absences"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adminprofile",
            name="country",
            field=models.CharField(
                default="CM", max_length=200, verbose_name="Country"
            ),
        ),
    ]
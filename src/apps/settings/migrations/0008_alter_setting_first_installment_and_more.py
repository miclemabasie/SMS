# Generated by Django 5.0 on 2024-07-05 09:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("settings", "0007_setting_first_installment_setting_second_installment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="setting",
            name="first_installment",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="setting",
            name="second_installment",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
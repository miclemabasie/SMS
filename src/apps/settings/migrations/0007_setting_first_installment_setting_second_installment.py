# Generated by Django 5.0 on 2024-07-05 09:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("settings", "0006_alter_setting_school_favicon"),
    ]

    operations = [
        migrations.AddField(
            model_name="setting",
            name="first_installment",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="setting",
            name="second_installment",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]

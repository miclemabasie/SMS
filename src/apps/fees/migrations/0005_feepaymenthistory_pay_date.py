# Generated by Django 5.0 on 2024-03-15 23:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fees", "0004_remove_feepaymenthistory_fee_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="feepaymenthistory",
            name="pay_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

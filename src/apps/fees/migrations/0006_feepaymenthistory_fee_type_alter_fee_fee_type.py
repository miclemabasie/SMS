# Generated by Django 5.0 on 2024-03-16 00:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fees", "0005_feepaymenthistory_pay_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="feepaymenthistory",
            name="fee_type",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="FeeType"
            ),
        ),
        migrations.AlterField(
            model_name="fee",
            name="fee_type",
            field=models.CharField(
                choices=[
                    ("pta", "PTA Fee"),
                    ("school_fees", "School Fees"),
                    ("other", "Other"),
                ],
                default="school_fees",
                max_length=20,
                verbose_name="Fee Type",
            ),
        ),
    ]

# Generated by Django 5.0 on 2024-07-27 13:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0006_alter_reportgenerationstatus_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportgenerationstatus",
            name="file_name",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]

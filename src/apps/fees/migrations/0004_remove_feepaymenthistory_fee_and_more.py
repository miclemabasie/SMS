# Generated by Django 5.0 on 2024-03-15 22:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fees", "0003_feepaymenthistory"),
        ("staff", "0002_adminprofile_is_admin_adminprofile_matricule"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feepaymenthistory",
            name="fee",
        ),
        migrations.AddField(
            model_name="feepaymenthistory",
            name="amount_paid",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="feepaymenthistory",
            name="collected_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="staff.adminprofile",
            ),
        ),
        migrations.AlterField(
            model_name="fee",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="fee",
            name="target",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
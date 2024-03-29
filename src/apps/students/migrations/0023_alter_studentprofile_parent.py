# Generated by Django 5.0 on 2024-03-26 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0006_remove_parentprofile_last_name"),
        ("students", "0022_alter_mark_student"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentprofile",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="childrend",
                to="profiles.parentprofile",
            ),
        ),
    ]

# Generated by Django 5.0 on 2024-06-28 00:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leave", "0003_adminleave_is_active_studentleave_is_active_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="adminleave",
            name="accepted",
        ),
        migrations.RemoveField(
            model_name="adminleave",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="studentleave",
            name="accepted",
        ),
        migrations.RemoveField(
            model_name="studentleave",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="teacherleave",
            name="accepted",
        ),
        migrations.RemoveField(
            model_name="teacherleave",
            name="is_active",
        ),
        migrations.AddField(
            model_name="adminleave",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                    ("Expired", "Expired"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="studentleave",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                    ("Expired", "Expired"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="teacherleave",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                    ("Expired", "Expired"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
    ]

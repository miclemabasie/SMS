# Generated by Django 5.0 on 2024-06-29 00:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leave", "0004_remove_adminleave_accepted_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="adminleave",
            name="approval_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="studentleave",
            name="approval_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="teacherleave",
            name="approval_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="adminleave",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="studentleave",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="teacherleave",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
    ]

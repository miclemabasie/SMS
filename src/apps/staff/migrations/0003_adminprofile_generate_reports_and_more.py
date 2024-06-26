# Generated by Django 5.0 on 2024-06-02 19:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("staff", "0002_adminprofile_is_admin_adminprofile_matricule"),
    ]

    operations = [
        migrations.AddField(
            model_name="adminprofile",
            name="generate_reports",
            field=models.BooleanField(default=False, verbose_name="Generate Reports"),
        ),
        migrations.AddField(
            model_name="adminprofile",
            name="manage_admins",
            field=models.BooleanField(
                default=False, verbose_name="Manage Administrators"
            ),
        ),
        migrations.AddField(
            model_name="adminprofile",
            name="manage_sessions",
            field=models.BooleanField(default=False, verbose_name="Manage Sessions"),
        ),
        migrations.AddField(
            model_name="adminprofile",
            name="manage_students",
            field=models.BooleanField(default=False, verbose_name="Manage Students"),
        ),
        migrations.AddField(
            model_name="adminprofile",
            name="manage_subjects",
            field=models.BooleanField(default=False, verbose_name="Manage Subjects"),
        ),
        migrations.AddField(
            model_name="adminprofile",
            name="manage_teachers",
            field=models.BooleanField(default=False, verbose_name="Manage Teachers"),
        ),
    ]

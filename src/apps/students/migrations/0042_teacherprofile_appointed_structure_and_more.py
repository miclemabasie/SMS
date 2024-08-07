# Generated by Django 5.0 on 2024-07-04 15:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0041_subject_has_class"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacherprofile",
            name="appointed_structure",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Appointed Structure",
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="appointment_decision_reference",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Reference of the Appointment Decision",
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="career_category",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Career Category"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="career_echelon",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Career Echelon"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="career_grade",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Career Grade"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="career_index",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Career Index"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="corps",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Corps"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="date_recruitement_public_service",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Date of Recruitement into Public Service",
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="division_of_origin",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Division of Origin"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="indemnity_situation",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Indemnity Situation",
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="longivity_in_administration",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Longivity in Administration",
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="longivity_of_post",
            field=models.CharField(
                blank=True,
                help_text="Longivity of post in years",
                max_length=200,
                null=True,
                verbose_name="Longivity of Post",
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="payroll_category_solde",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Payroll Category Solde",
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="payroll_echelon",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Payroll Echelon"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="payroll_grade",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Payroll Grade"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="payroll_index",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Payroll Index"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="possition_rank",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Position Rank"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="region_of_origin",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Region of Origin"
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="serivice",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Central", "Central"),
                    ("Deconcentrated", "Deconcentrated"),
                    ("Attached", "Attached"),
                    ("External", "External"),
                    ("Other", "Other"),
                ],
                default="Other",
                max_length=20,
                null=True,
                verbose_name="Service",
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="sub_division_of_origin",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Sub Division of Origin",
            ),
        ),
        migrations.AddField(
            model_name="teacherprofile",
            name="town",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Town"
            ),
        ),
    ]

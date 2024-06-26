# Generated by Django 5.0 on 2024-06-25 21:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0030_studenttempcreateprofile_teachertempcreateprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacherprofile",
            name="classes",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="teachers", to="students.class"
            ),
        ),
    ]

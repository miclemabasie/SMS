# Generated by Django 5.0 on 2024-03-13 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0016_subject_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subject",
            name="klass",
        ),
        migrations.AddField(
            model_name="class",
            name="subjects",
            field=models.ManyToManyField(
                blank=True, related_name="subjects", to="students.subject"
            ),
        ),
    ]

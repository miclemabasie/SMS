# Generated by Django 5.0 on 2024-03-23 20:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("terms", "0009_alter_examinationsession_is_current"),
    ]

    operations = [
        migrations.AlterField(
            model_name="examinationsession",
            name="exam_session",
            field=models.CharField(
                choices=[
                    ("First Sequence", "First Sequence"),
                    ("Second Sequence", "Second Sequence"),
                    ("Third Sequence", "Third Sequence"),
                    ("Fourth Sequence", "Fourth Sequence"),
                    ("Fifth Sequence", "Fifth Sequence"),
                    ("Sixth Sequence", "Sixth Sequence"),
                    ("Seventh Sequence", "Seventh Sequence"),
                ],
                default="First Sequence",
                max_length=20,
                verbose_name="Exam Sequence",
            ),
        ),
    ]

# Generated by Django 5.0 on 2024-03-20 21:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("terms", "0007_alter_term_term"),
    ]

    operations = [
        migrations.AddField(
            model_name="examinationsession",
            name="is_current",
            field=models.BooleanField(default=True),
        ),
    ]

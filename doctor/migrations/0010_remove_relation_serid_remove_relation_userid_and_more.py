# Generated by Django 4.1.1 on 2023-01-16 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0009_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="relation",
            name="SerId",
        ),
        migrations.RemoveField(
            model_name="relation",
            name="UserId",
        ),
        migrations.DeleteModel(
            name="Doctor",
        ),
        migrations.DeleteModel(
            name="Relation",
        ),
        migrations.DeleteModel(
            name="Service",
        ),
    ]

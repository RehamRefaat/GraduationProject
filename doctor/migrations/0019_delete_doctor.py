# Generated by Django 4.1.1 on 2023-02-03 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0018_alter_doctor_options_remove_doctor_input"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Doctor",
        ),
    ]

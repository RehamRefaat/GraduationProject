# Generated by Django 4.1.1 on 2023-02-01 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctor", "0016_alter_doctor_input"),
    ]

    operations = [
        migrations.RenameField(
            model_name="doctor",
            old_name="FirstName",
            new_name="Name",
        ),
        migrations.RemoveField(
            model_name="doctor",
            name="LastName",
        ),
        migrations.AlterField(
            model_name="doctor",
            name="Input",
            field=models.ImageField(upload_to="input/%y/%m/%d"),
        ),
    ]

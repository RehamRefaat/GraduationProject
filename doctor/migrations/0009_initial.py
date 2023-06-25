# Generated by Django 4.1.1 on 2023-01-16 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("doctor", "0008_remove_relation_userid_delete_doctor_delete_relation"),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("FirstName", models.CharField(max_length=80)),
                ("LastName", models.CharField(max_length=80)),
                ("Gender", models.CharField(max_length=6)),
                ("Country", models.CharField(max_length=50)),
                ("City", models.CharField(max_length=50)),
                ("Specialist", models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Input", models.CharField(max_length=500)),
                ("Output", models.CharField(max_length=500)),
                ("Processnumber", models.IntegerField()),
                ("Flag", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Relation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateTimeField(auto_now_add=True)),
                (
                    "SerId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="doctor.service"
                    ),
                ),
                (
                    "UserId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="doctor.doctor"
                    ),
                ),
            ],
        ),
    ]

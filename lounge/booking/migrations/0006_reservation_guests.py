# Generated by Django 4.1.6 on 2023-02-18 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0005_rename_appointment_reservation"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="guests",
            field=models.CharField(
                choices=[
                    ("1", "1 Guest"),
                    ("2", "2 Guests"),
                    ("3", "3 Guests"),
                    ("4", "4 Guests"),
                    ("5", "5 Guests"),
                    ("6", "6 Guests"),
                    ("6", "7 Guests"),
                ],
                default="1",
                max_length=1,
            ),
        ),
    ]
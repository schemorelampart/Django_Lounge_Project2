# Generated by Django 4.1.6 on 2023-02-17 21:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("booking", "0003_reservations_delete_appointment"),
    ]

    operations = [
        migrations.RenameModel(old_name="Reservations", new_name="appointment",),
    ]

# Generated by Django 4.0.4 on 2022-05-26 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0003_alter_measurement_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurement',
            old_name='current_location',
            new_name='starting_location',
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-26 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0002_alter_measurement_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='created',
            field=models.TimeField(auto_now=True),
        ),
    ]

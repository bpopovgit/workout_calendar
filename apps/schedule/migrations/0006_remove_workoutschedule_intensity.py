# Generated by Django 5.1.3 on 2024-12-15 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_workoutschedule_intensity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutschedule',
            name='intensity',
        ),
    ]

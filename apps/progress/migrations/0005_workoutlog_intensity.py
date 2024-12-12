# Generated by Django 5.1.3 on 2024-12-11 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0004_alter_workoutlog_date_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutlog',
            name='intensity',
            field=models.CharField(choices=[('Low', 'Low'), ('Moderate', 'Moderate'), ('High', 'High')], default='Moderate', max_length=50),
        ),
    ]

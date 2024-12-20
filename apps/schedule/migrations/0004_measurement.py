# Generated by Django 5.1.3 on 2024-12-11 12:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_workoutschedule_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveIntegerField()),
                ('year', models.PositiveIntegerField()),
                ('weight', models.FloatField(blank=True, null=True)),
                ('chest', models.FloatField(blank=True, null=True)),
                ('arm', models.FloatField(blank=True, null=True)),
                ('waist', models.FloatField(blank=True, null=True)),
                ('hips', models.FloatField(blank=True, null=True)),
                ('thighs', models.FloatField(blank=True, null=True)),
                ('calf', models.FloatField(blank=True, null=True)),
                ('bmi', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-15 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='goals',
            new_name='progress',
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-17 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofile',
            old_name='pno',
            new_name='phone',
        ),
    ]

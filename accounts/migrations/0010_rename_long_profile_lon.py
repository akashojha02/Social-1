# Generated by Django 3.2.5 on 2022-01-19 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20220117_0000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='long',
            new_name='lon',
        ),
    ]

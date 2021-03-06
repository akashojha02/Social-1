# Generated by Django 3.2.5 on 2022-01-06 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20220106_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend_request',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='accounts.user'),
        ),
        migrations.AlterField(
            model_name='friend_request',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='accounts.user'),
        ),
    ]

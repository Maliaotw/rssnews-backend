# Generated by Django 3.0.9 on 2022-04-10 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20220409_1714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='source',
            old_name='status',
            new_name='enable',
        ),
    ]

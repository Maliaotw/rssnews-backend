# Generated by Django 3.0.9 on 2022-02-27 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial_squashed_0002_auto_20220220_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='thumbnail',
            field=models.URLField(blank=True, default=''),
        ),
    ]

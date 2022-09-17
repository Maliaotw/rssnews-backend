# Generated by Django 3.0.9 on 2022-09-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20220626_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='published_parsed',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AddIndex(
            model_name='news',
            index=models.Index(fields=['published_parsed'], name='app_news_publish_de20e1_idx'),
        ),
    ]

# Generated by Django 2.0.6 on 2018-11-24 06:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0003_auto_20181123_2208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shop',
            options={},
        ),
        migrations.AddField(
            model_name='shop',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2018, 11, 24, 6, 50, 22, 429122, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='auth_image',
            field=models.ImageField(blank=True, upload_to='auth/%y/%m/%d'),
        ),
    ]

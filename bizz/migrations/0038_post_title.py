# Generated by Django 2.0.6 on 2019-03-03 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0037_post_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=250),
        ),
    ]

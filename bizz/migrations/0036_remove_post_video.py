# Generated by Django 2.0.6 on 2019-02-18 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0035_post_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='video',
        ),
    ]
# Generated by Django 2.0.6 on 2019-02-18 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0036_remove_post_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, default='', null=True, upload_to='post_videos/%y/%m/%d'),
        ),
    ]

# Generated by Django 2.0.6 on 2019-03-03 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0038_post_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]

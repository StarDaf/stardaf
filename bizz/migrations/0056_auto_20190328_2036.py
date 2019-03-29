# Generated by Django 2.0.6 on 2019-03-29 03:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bizz', '0055_auto_20190328_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='question',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='users_hate',
            field=models.ManyToManyField(blank=True, related_name='post_hated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='post_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 2.0.6 on 2018-12-05 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ('-created',)},
        ),
    ]

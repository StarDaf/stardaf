# Generated by Django 2.0.6 on 2018-11-26 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]

# Generated by Django 2.0.6 on 2018-12-19 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0023_auto_20181217_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', max_length=500, unique=True),
        ),
    ]

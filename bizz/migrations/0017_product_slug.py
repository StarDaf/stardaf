# Generated by Django 2.0.6 on 2018-12-05 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0016_product_total_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', max_length=500),
        ),
    ]

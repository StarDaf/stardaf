# Generated by Django 2.0.6 on 2019-02-28 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], default='1', max_length=5),
        ),
    ]
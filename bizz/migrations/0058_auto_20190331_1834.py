# Generated by Django 2.0.6 on 2019-04-01 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0057_auto_20190331_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]

# Generated by Django 2.0.6 on 2018-11-30 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0011_auto_20181129_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, upload_to='products/%y/%m/%d'),
        ),
    ]

# Generated by Django 2.0.6 on 2018-11-24 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0006_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/%y/%m/%d'),
        ),
    ]

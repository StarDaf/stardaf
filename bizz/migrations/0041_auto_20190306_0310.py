# Generated by Django 2.0.6 on 2019-03-06 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0040_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='business_address',
            field=models.CharField(choices=[('private', 'Private')], default='private', max_length=20),
        ),
    ]
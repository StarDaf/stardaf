# Generated by Django 2.0.6 on 2018-11-25 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='name',
            new_name='full_name',
        ),
    ]

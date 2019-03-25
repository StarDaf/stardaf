# Generated by Django 2.0.6 on 2019-03-24 23:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bizz', '0052_auto_20190323_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='users_hate',
            field=models.ManyToManyField(blank=True, related_name='product_hated', to=settings.AUTH_USER_MODEL),
        ),
    ]

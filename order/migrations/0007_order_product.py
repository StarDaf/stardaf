# Generated by Django 2.0.6 on 2019-03-01 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0037_post_video'),
        ('order', '0006_auto_20190228_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='bizz.Product'),
        ),
    ]

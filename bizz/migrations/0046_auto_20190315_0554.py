# Generated by Django 2.0.6 on 2019-03-15 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0045_auto_20190313_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='Bank',
            field=models.CharField(choices=[('Access Bank Plc', 'Access Bank Plc'), ('Citibank Nigeria Limited', 'Citibank Nigeria Limited'), ('Diamond Bank Plc', 'Diamond Bank Plc'), ('Ecobank Nigeria Plc', 'Ecobank Nigeria Plc'), ('Fidelity Bank Plc', 'Fidelity Bank Plc'), ('First City Monument Bank Plc', 'First City Monument Bank Plc'), ('First Bank Limited', 'First Bank Limited'), ('Guaranty Trust Bank Plc', 'Guaranty Trust Bank Plc'), ('Heritage Banking Company Limited', 'Heritage Banking Company Limited'), ('JAIZ Bank Plc', 'JAIZ Bank Plc'), ('Keystone Bank Limited', 'Keystone Bank Limited'), ('Polaris Bank Limited', 'Polaris Bank Limited'), ('Providus Bank Limited', 'Providus Bank Limited'), ('Stanbic IBTC Bank Plc', 'Stanbic IBTC Bank Plc'), ('Standard Chartered', 'Standard Chartered'), ('Sterling Bank Plc', 'Sterling Bank Plc'), ('SunTrust Bank Nigeria Limited', 'SunTrust Bank Nigeria Limited'), ('Union Bank of Nigeria Plc', 'Union Bank of Nigeria Plc'), ('United Bank for Africa Plc', 'United Bank for Africa Plc'), ('Unity Bank Plc', 'Unity Bank Plc'), ('Wema Bank Plc', 'Wema Bank Plc'), ('Zenith Bank Plc', 'Zenith Bank Plc')], default='', max_length=250),
        ),
    ]

# Generated by Django 2.0.9 on 2019-07-21 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yekpay', '0017_auto_20190313_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='callback_url',
            field=models.CharField(max_length=1000),
        ),
    ]
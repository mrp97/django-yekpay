# Generated by Django 3.2.4 on 2021-06-22 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yekpay', '0020_transaction_additional_callback_params'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='additional_callback_params',
            field=models.JSONField(blank=True, default={}, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
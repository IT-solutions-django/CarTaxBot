# Generated by Django 5.1.7 on 2025-03-26 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0002_currency_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('JPY', 'JPY'), ('CNY', 'CNY'), ('KRW', 'KRW'), ('RUB', 'RUB')], max_length=3, verbose_name='Код'),
        ),
    ]

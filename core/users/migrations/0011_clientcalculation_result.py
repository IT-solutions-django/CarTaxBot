# Generated by Django 5.1.7 on 2025-03-28 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_clientcalculation_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcalculation',
            name='result',
            field=models.TextField(default='', verbose_name='Результат'),
            preserve_default=False,
        ),
    ]

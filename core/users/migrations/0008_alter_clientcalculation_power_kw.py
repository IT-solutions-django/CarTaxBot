# Generated by Django 5.1.7 on 2025-03-27 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_clientcalculation_car_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientcalculation',
            name='power_kw',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Мощность (кВт, за 30 мин)'),
        ),
    ]

# Generated by Django 5.1.7 on 2025-03-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_feedbackrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackrequest',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Обработано'),
        ),
    ]

from django.db import models


class Currency(models.Model): 
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('JPY', 'JPY'),
        ('CNY', 'CNY'),
        ('KRW', 'KRW'),
    ]

    name = models.CharField('Название', max_length=50)
    code = models.CharField('Код', max_length=3, choices=CURRENCY_CHOICES)
    exchange_rate = models.FloatField('Курс', default=0)

    class Meta: 
        verbose_name = 'валюта'
        verbose_name_plural = 'валюты'
from django.db import models


class Reciever(models.Model): 
    telegram_id = models.CharField('Telegram ID', max_length=15) 

    class Meta: 
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели' 

    def __str__(self):
        return f'{self.telegram_id}'
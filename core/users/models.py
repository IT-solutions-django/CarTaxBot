from django.db import models


class ClientStatus(models.Model): 
    name = models.CharField('Название', max_length=50)

    class Meta: 
        verbose_name = 'статус клиента'
        verbose_name_plural = 'Статусы клиентов'

    def __str__(self):
        return f'{self.name}'
    
    def get_start_status(): 
        status, _ = ClientStatus.objects.get_or_create(name='start')
        return status
    
    def get_calc_status(): 
        status, _ = ClientStatus.objects.filter(name='calc')
        return status


class Client(models.Model): 
    telegram_id = models.CharField('Telegram ID', max_length=15) 
    name = models.CharField('Имя', null=True, blank=True, max_length=50) 
    phone = models.CharField('Телефон', null=True, blank=True, max_length=50)
    status = models.ForeignKey(verbose_name='Статус', to=ClientStatus, on_delete=models.CASCADE, related_name='clients')

    class Meta: 
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'Клиент {self.telegram_id}'
    

class FeedbackRequest(models.Model): 
    name = models.CharField('Имя', null=True, blank=True, max_length=50) 
    phone = models.CharField('Телефон', null=True, blank=True, max_length=50)
    client = models.ForeignKey(verbose_name='Клиент', to=Client, on_delete=models.CASCADE)
    is_closed = models.BooleanField('Обработано', default=False)

    class Meta: 
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return f'Клиент {self.client} | {self.name} | {self.phone}'


class ClientCalculation(models.Model): 
    client = models.ForeignKey(verbose_name='Клиент', to=Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True, max_length=50) 
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)  
    age = models.CharField('Возраст', max_length=20)  
    volume = models.FloatField('Объём двигателя')  
    currency = models.CharField('Валюта', max_length=3)  
    engine_type = models.CharField('Тип двигателя', max_length=50)  

    class Meta: 
        verbose_name = 'расчёт'
        verbose_name_plural = 'расчёты'
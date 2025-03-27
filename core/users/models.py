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
        status, _ = ClientStatus.objects.get_or_create(name='calc')
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
        return f"{f'{self.name} (+{self.phone})' if self.name else f'Telegram ID {self.telegram_id}'}"
    

class FeedbackRequest(models.Model): 
    name = models.CharField('Имя', null=True, blank=True, max_length=50) 
    phone = models.CharField('Телефон', null=True, blank=True, max_length=50)
    client = models.ForeignKey(verbose_name='Клиент', to=Client, on_delete=models.CASCADE)
    is_closed = models.BooleanField('Обработано', default=False)

    class Meta: 
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return f'Заявка от {self.client}'


class ClientCalculation(models.Model): 
    client = models.ForeignKey(verbose_name='Клиент', to=Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True, max_length=50) 
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)  
    age = models.CharField('Возраст', max_length=20)  
    volume = models.FloatField('Объём двигателя')  
    currency = models.CharField('Валюта', max_length=3)  
    engine_type = models.CharField('Тип двигателя', max_length=50)  
    car_type = models.CharField('Тип транспортного средства', max_length=50) 
    power_kw = models.CharField('Мощность (кВт, за 30 мин)', max_length=10, null=True, blank=True)

    class Meta: 
        verbose_name = 'расчёт'
        verbose_name_plural = 'расчёты'

    def __str__(self):
        return f'Расчёт пошлины {self.client.telegram_id} ({self.created_at.strftime("%d.%m.%Y")})'
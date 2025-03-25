from django.db import models


class ClientStatus(models.Model): 
    name = models.CharField('Название', max_length=50)

    class Meta: 
        verbose_name = 'статус клиента'
        verbose_name_plural = 'Статусы клиентов'

    def __str__(self):
        return f'{self.name}'
    
    def get_primary_contact_status(): 
        return ClientStatus.objects.filter(name='Написал боту').first()
    
    def get_calculated_tall_status(): 
        return ClientStatus.objects.filter(name='Рассчитал пошлину').first()
    
    def get_left_contacts_status(): 
        return ClientStatus.objects.filter(name='Оставил контактные данные').first()


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
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True, max_length=50)

    class Meta: 
        verbose_name = 'расчёт'
        verbose_name_plural = 'расчёты'
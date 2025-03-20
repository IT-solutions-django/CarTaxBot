from django.contrib import admin
from .models import Client, ClientStatus, ClientCalculation


@admin.register(Client) 
class ClientAdmin(admin.ModelAdmin): 
    list_display = ['telegram_id', 'name', 'phone']


@admin.register(ClientStatus) 
class ClientStatusAdmin(admin.ModelAdmin): 
    list_display = ['name']
from django.contrib import admin
from .models import Client, ClientStatus, ClientCalculation, FeedbackRequest


@admin.register(Client) 
class ClientAdmin(admin.ModelAdmin): 
    list_display = ['telegram_id', 'name', 'phone']


@admin.register(ClientStatus) 
class ClientStatusAdmin(admin.ModelAdmin): 
    list_display = ['name']


@admin.register(FeedbackRequest) 
class FeedbackRequestAdmin(admin.ModelAdmin): 
    list_display = ['client', 'name', 'phone', 'is_closed']
    list_filter = ['is_closed']
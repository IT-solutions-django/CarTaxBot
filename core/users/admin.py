from django.contrib import admin
from .models import (
    Client, 
    ClientStatus, 
    ClientCalculation, 
    FeedbackRequest,
)


@admin.register(Client) 
class ClientAdmin(admin.ModelAdmin): 
    list_display = ['telegram_id', 'name', 'phone', 'status']


@admin.register(ClientStatus) 
class ClientStatusAdmin(admin.ModelAdmin): 
    list_display = ['name']


@admin.register(FeedbackRequest) 
class FeedbackRequestAdmin(admin.ModelAdmin): 
    list_display = ['client', 'name', 'phone', 'is_closed']
    list_filter = ['is_closed']


@admin.register(ClientCalculation) 
class ClientCalculationAdmin(admin.ModelAdmin): 
    list_display = ['client', 'age', 'volume', 'currency', 'engine_type', 'created_at', 'price']
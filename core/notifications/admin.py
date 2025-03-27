from django.contrib import admin
from .models import Reciever


@admin.register(Reciever) 
class RecieverAdmin(admin.ModelAdmin): 
    list_display = ['telegram_id']
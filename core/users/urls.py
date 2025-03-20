from django.urls import path
from .views import *


app_name = 'users'


urlpatterns = [
    path('add-client/', CreateClientView.as_view(), name='add_client'),
]
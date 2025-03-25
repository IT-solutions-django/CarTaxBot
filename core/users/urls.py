from django.urls import path
from .views import *


app_name = 'users'


urlpatterns = [
    path('add-client/', CreateClientView.as_view(), name='add_client'),
    path('leave-request/', SetContactDataView.as_view(), name='set_contact_data'),
    path('add-calculation/', AddClientCalculationView.as_view(), name='add_calculation'),
]
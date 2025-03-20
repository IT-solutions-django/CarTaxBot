from celery import shared_task
from .services import update_exchange_rates


@shared_task
def update_currencies_task() -> None: 
    update_exchange_rates()


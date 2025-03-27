from .models import Reciever
import requests
import os
from dotenv import load_dotenv


load_dotenv()


TELEGRAM_BOT_API_KEY = os.getenv('API_TOKEN')


def send_telegram_message_for_all(message: str) -> None: 
    telegram_ids = Reciever.objects.values_list('telegram_id', flat=True)

    for telegram_id in telegram_ids:
        requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage',
            json={
                'chat_id': telegram_id,
                'text': message,
            }
        )
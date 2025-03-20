import os 
from celery import Celery 
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 


app = Celery('app') 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_currencies': {
        'task': 'currencies.tasks.update_currencies_task',
        'schedule': crontab(hour=12, minute=0),
    }
}

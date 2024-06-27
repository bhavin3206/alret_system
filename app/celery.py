# myproject/celery.py

from celery import Celery
from celery.schedules import crontab

app = Celery('app')

app.conf.beat_schedule = {
    'check-prices-every-minute': {
        'task': 'myapp.tasks.check_prices_and_notify',
        'schedule': crontab(minute='*/1'),  # Every minute
    },
}



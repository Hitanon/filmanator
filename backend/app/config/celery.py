import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.develop')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_expire_sessions_every_hour': {
        'task': 'questionnaire.tasks.delete_expire_sessions',
        'schedule': crontab(hour='*/1'),
    },
}

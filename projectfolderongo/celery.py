import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectfolderongo.settings')
app = Celery('ongo_project')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_daily_report': {
        'task': 'send_daily_report',
        # 'schedule': crontab(minute=0, hour=21),
        'schedule': 30.0,
    },
}
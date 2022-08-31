import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_management.settings')

app = Celery('project_management')
app.conf.beat_schedule = {}

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
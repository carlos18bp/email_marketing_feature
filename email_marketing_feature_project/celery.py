from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_marketing_feature_project.settings')

# Create an instance of the Celery application
app = Celery('email_marketing_feature_project')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all registered Django apps
app.autodiscover_tasks()

# Celery Beat schedule configuration
app.conf.beat_schedule = {
    'send-scheduled-emails-every-day': {
        'task': 'email_marketing_feature_app.tasks.send_scheduled_emails',
        'schedule': crontab(hour=12, minute=0),  # Run every day at noon
    },
}

# Set the timezone for Celery
app.conf.timezone = 'UTC'

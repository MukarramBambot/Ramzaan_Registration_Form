"""
Celery configuration for Azaan & Takhbira Duty Management.
Handles background task processing and scheduled reminders.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')

# Create Celery app
app = Celery('sherullah_service')

# Load config from Django settings, using CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule - Periodic Tasks
app.conf.beat_schedule = {
    # Process pending reminders every 15 minutes
    'process-reminders-every-15-min': {
        'task': 'registrations.process_reminders',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
        'options': {
            'expires': 600,  # Task expires after 10 minutes
        }
    },
    
    # Cleanup old reminders daily at 2 AM
    'cleanup-old-reminders-daily': {
        'task': 'registrations.cleanup_old_reminders',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2:00 AM
        'options': {
            'expires': 3600,
        }
    },

    # Process voice reminders every 5 minutes
    'process-voice-reminders-every-5-min': {
        'task': 'registrations.process_due_reminder_calls',
        'schedule': crontab(minute='*/5'),
        'options': {
            'expires': 200,
        }
    },
}

# Celery Configuration
app.conf.update(
    # Task settings
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',  # IST timezone
    enable_utc=False,
    
    # Result backend
    result_expires=3600,  # Results expire after 1 hour
    
    # Task routing
    task_routes={
        'registrations.*': {'queue': 'default'},
    },
    
    # Default queue (worker will listen to this by default)
    task_default_queue='default',
    task_default_exchange='default',
    task_default_routing_key='default',
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)


@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup"""
    print(f'Request: {self.request!r}')

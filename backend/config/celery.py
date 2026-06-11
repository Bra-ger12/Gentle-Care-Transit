"""
Celery configuration for Gentle Care Transit.
"""

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('gentle_care_transit')

# Load configuration from Django settings, all configuration keys will be prefixed with `CELERY_`
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django app configs.
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    # Check for pending bookings every 5 minutes
    'check-pending-bookings': {
        'task': 'bookings.tasks.check_pending_bookings',
        'schedule': crontab(minute='*/5'),
    },
    # Send reminders for upcoming appointments every hour
    'send-appointment-reminders': {
        'task': 'notifications.tasks.send_appointment_reminders',
        'schedule': crontab(minute=0),
    },
    # Update driver availability status
    'update-driver-status': {
        'task': 'drivers.tasks.update_availability_status',
        'schedule': crontab(minute='*/10'),
    },
    # Generate daily reports at midnight
    'generate-daily-reports': {
        'task': 'reports.tasks.generate_daily_report',
        'schedule': crontab(hour=0, minute=0),
    },
    # Cleanup old location data (keep last 30 days)
    'cleanup-old-locations': {
        'task': 'trips.tasks.cleanup_old_locations',
        'schedule': crontab(hour=2, minute=0),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

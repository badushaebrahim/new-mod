import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog22.settings')



__all__ = ('blog22',)
celery_app = Celery('blog22')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
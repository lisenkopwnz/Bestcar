from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitecars.settings')

app = Celery('sitecars')

# Настройка брокера
app.config_from_object('django.conf:settings', namespace='CELERY')


# Автоматический поиск задач
app.autodiscover_tasks()
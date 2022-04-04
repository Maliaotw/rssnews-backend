import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("web")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['app'])

app.conf.timezone = 'Asia/Taipei'


# app.
app.conf.beat_schedule = {
    '[Telegram] 定期爬取RSS': {
        'task': 'app.tasks.crawl_news',
        'args': (),
        'schedule': crontab(minute='*/5', hour='*'),
    },
    '[Telegram] 定期同步入庫': {
        'task': 'app.tasks.sync_news',
        'args': (),
        'schedule': crontab(minute='*/5', hour='*'),
    },
    '[Telegram] 定期發送訊息': {
        'task': 'app.tasks.send_news',
        'args': (),
        'schedule': crontab(minute='*/5', hour='*'),
    },

}


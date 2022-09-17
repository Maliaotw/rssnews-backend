import os

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

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
app.conf.task_soft_time_limit = 300
app.conf.task_time_limit = 600
app.conf.worker_max_tasks_per_child = 40
app.conf.broker_heartbeat = 0
app.conf.task_acks_late = True

app.conf.broker_transport_options = {'visibility_timeout': 43200}

app.conf.task_default_queue = 'rss'
app.conf.task_queues = (
    Queue('rss'),
    # Queue('rss', Exchange('rss'), routing_key='default'),
    # Queue('videos',  Exchange('media'),   routing_key='media.video'),
    # Queue('images',  Exchange('media'),   routing_key='media.image'),
)



@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from app.tasks import crawl_news, sync_news, send_news


    sender.add_periodic_task(crontab(minute='*/5', hour='*'), crawl_news.s(), name='[Telegram] 定期爬取RSS',expires=10)

    sender.add_periodic_task(crontab(minute='*/5', hour='*'), sync_news.s(), name='[Telegram] 定期同步入庫',expires=10)

    sender.add_periodic_task(crontab(minute='*/5', hour='*'), send_news.s(), name='[Telegram] 定期發送訊息',expires=10)



#
# app.conf.beat_schedule = {
#     '[Telegram] 定期爬取RSS': {
#         'task': 'app.tasks.crawl_news',
#         'args': (),
#         'schedule': crontab(minute='*/5', hour='*'),
#     },
#     '[Telegram] 定期同步入庫': {
#         'task': 'app.tasks.sync_news',
#         'args': (),
#         'schedule': crontab(minute='*/5', hour='*'),
#     },
#     '[Telegram] 定期發送訊息': {
#         'task': 'app.tasks.send_news',
#         'args': (),
#         'schedule': crontab(minute='*/5', hour='*'),
#     },
#
# }


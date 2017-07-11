from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from celery.signals import celeryd_init, worker_ready

# set the default Django settings module for the 'celery' program.
from tw.models import FetchStream, MessageBoot
from tw_analysis.settings.local_settings import REDIS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tw_analysis.settings.base')

app = Celery('tw_analysis')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task.py modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.result_backend = REDIS


# app.conf.beat_schedule = {
#     'tweet_cloud': {
#         'task': 'tw.tasks.tweet_cloud',
#         'schedule': crontab(minute=0, hour='*/6')
#     },
#     "keep_alive": {
#         'task': 'tw.tasks.keep_alive',
#         'schedule': 300.0,
#     },
#     'auto_follow_back': {
#         'task': 'tw.tasks.auto_follow_back',
#         'schedule': 1800.0,
#     },
# }


@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
        # message = MessageBoot()
        # message.send()
        stream = FetchStream
        stream.fetch()

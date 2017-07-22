from __future__ import absolute_import, unicode_literals
import os
import time
from celery import Celery, shared_task
from celery.schedules import crontab
from celery.signals import celeryd_init, worker_ready, worker_init

# set the default Django settings module for the 'celery' program.
from celery.utils.dispatch import signal

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


@shared_task
def start_up():
    # message = MessageBoot()
    # message.send()
    stream = FetchStream
    stream.fetch()



# app.conf.beat_schedule = {
#
#     "keep_alive": {
#         'task': 'tw.tasks.keep_alive',
#         'schedule': 1.0,
#     },
#
# }

@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
        start_up.apply_async()
        print('hello')

import datetime

import jdatetime
from django.core.management.base import BaseCommand
from tw.models import FetchTweets
from django_celery_beat.models import PeriodicTask, PeriodicTasks


class Command(BaseCommand):
    help = 'fetch today tweets'

    def handle(self, *args, **options):
        print(datetime.datetime.now().strftime('%d-%b-%Y | %H:%M:%S'))
        yesterday = datetime.date.today() - datetime.timedelta(1)
        date = jdatetime.date.fromgregorian(date=yesterday)
        print(date)
        status_text = "ابر کلمات از {} تویت در تاریخ {}".format(50,
                                                                date.strftime(
                                                                    "%d-%b-%Y "))
        print(status_text)

        # task_update = PeriodicTask.objects.all()
        # task_update.update(last_run_at=None)
        # # task_update.changed()

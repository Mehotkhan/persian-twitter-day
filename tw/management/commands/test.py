import datetime

import pytz
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'fetch today tweets'

    def handle(self, *args, **options):
        current_tz = timezone.get_current_timezone()
        # tz = timezone('America/St_Johns')
        time = datetime.datetime.strptime('Mon Jul 03 00:48:19 +0000 2017',
                                          '%a %b %d %H:%M:%S +0000 %Y')

        print(pytz.utc.localize(time, is_dst=None).astimezone(current_tz))

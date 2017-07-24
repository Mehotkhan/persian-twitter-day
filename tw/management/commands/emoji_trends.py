from django.core.management.base import BaseCommand
from tw.views import EmojiTrend


class Command(BaseCommand):
    help = 'follow follower of user'

    def add_arguments(self, parser):
        parser.add_argument('from_date', type=int)
        parser.add_argument('from_time', type=int)

    def handle(self, *args, **options):
        from_date = None
        from_time = None
        if options['from_date'] == 0:
            from_date = None
        else:
            from_date = options['from_date']
        if options['from_time'] == 0:
            from_time = None
        else:
            from_time = options['from_time']

        EmojiTrend.send_data(from_date, from_time)

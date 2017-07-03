import parser
from django.core.management.base import BaseCommand
from tw.views import TweetCloud
from tw_analysis.settings.local_settings import api


class Command(BaseCommand):
    help = 'follow follower of user'

    def add_arguments(self, parser):
        parser.add_argument('from_date', type=float)
        parser.add_argument('from_time', type=float)
        parser.add_argument('max_words', type=int)

    def handle(self, *args, **options):
        from_date = None
        from_time = None
        if options['from_date'] == 0:
            from_date = None
        if options['from_time'] == 0:
            from_time = None
        command_cloud = TweetCloud()
        command_cloud.generate(from_date=from_date, from_time=from_time,
                               max_words=options['max_words'])
        command_cloud.send()

from multiprocessing import Pool
from django.core.management.base import BaseCommand
from tw.views import TweetCloud


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
        else:
            from_date = options['from_date']
        if options['from_time'] == 0:
            from_time = None
        else:
            from_time = options['from_time']

        pool = Pool(processes=4)
        pool.apply_async(TweetCloud.send_text_cloud, args=(from_date, from_time, options['max_words']))
        pool.close()
        pool.join()

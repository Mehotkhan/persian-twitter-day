from django.core.management.base import BaseCommand
from tw.models import FetchTweets


class Command(BaseCommand):
    help = 'fetch today tweets'

    def handle(self, *args, **options):
        fetcher = FetchTweets()
        fetcher.fetch()

from django.core.management.base import BaseCommand
from tw.views import TweetCloud
from tw_analysis.settings.local_settings import api


class Command(BaseCommand):
    help = 'follow follower of user'

    def handle(self, *args, **options):
        command_cloud = TweetCloud()
        command_cloud.generate()
        command_cloud.send()

import time
import sys
from django.core.management.base import BaseCommand
import tweepy
from tw_analysis.settings.local_settings import api


class Command(BaseCommand):
    help = 'follow follower of user'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def handle(self, *args, **options):
        friend_objects = [friend for friend in tweepy.Cursor(api.friends).items()]
        # create dictionaries based on id's for easy lookup
        friends = dict([(friend.id, friend) for friend in friend_objects])
        print("You follow", len(friends), "users")
        for friend in friends:
            for i in range(0, options['number']):
                try:
                    friend.unfollow()
                    print("unfollow", friend.screen_name)

                except tweepy.RateLimitError:
                    for i in range(2 * 60, 0, -1):
                        time.sleep(1)
                        sys.stdout.write("\r")
                        sys.stdout.write("{:2d} seconds remaining.".format(i))
                        sys.stdout.flush()
                    continue
                except tweepy.TweepError:
                    print('You are unable to follow more people at this time.')
                    exit()

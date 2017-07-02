import time
import sys
from django.core.management.base import BaseCommand
import tweepy
from tw_analysis.settings.local_settings import api


class Command(BaseCommand):
    help = 'follow follower of user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=str)

    def handle(self, *args, **options):
        friends = api.friends_ids(api.me().id)
        print("You follow", len(friends), "users")
        while True:
            try:
                user_follower = tweepy.Cursor(api.followers, screen_name=options['user_id']).items()
                # print('start following {} user'.format(len(list(user_follower))))
                for follower in user_follower:
                    if follower.id != api.me().id:
                        if follower.id in friends:
                            print("You already follow", follower.screen_name)
                        elif follower.id not in friends:
                            try:
                                follower.follow()
                                print("Started following", follower.screen_name)

                            except tweepy.RateLimitError:
                                for i in range(2 * 60, 0, -1):
                                    time.sleep(1)
                                    sys.stdout.write("\r")
                                    sys.stdout.write("{:2d} seconds remaining.".format(i))
                                    sys.stdout.flush()
                                continue
                            except tweepy.TweepError:
                                continue
                        else:
                            print('some error')
            except tweepy.RateLimitError:
                for i in range(2 * 60, 0, -1):
                    time.sleep(1)
                    sys.stdout.write("\r")
                    sys.stdout.write("{:2d} seconds remaining.".format(i))
                    sys.stdout.flush()
                # time.sleep(60 * 2)
                continue

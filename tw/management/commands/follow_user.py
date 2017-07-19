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
        friends_user = api.friends_ids(screen_name=options['user_id'])
        final_ids = [user for user in friends_user if user not in friends]
        if api.me().id in final_ids:
            final_ids.remove(api.me().id)
        print("You follow", len(friends), "users")
        print("friends_user", len(friends_user), "users")
        print("number of news follow = ", len(final_ids), "users")

        # while True:
        #     try:
        # user_follower = tweepy.Cursor(api.friends, screen_name=options['user_id']).items()
        # user_ids = []
        # print(len(user_follower))
        # print('start following {} user'.format(len(list(user_follower))))
        for follower in final_ids:
            try:
                api.create_friendship(follower)
                print("Started following", follower)

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

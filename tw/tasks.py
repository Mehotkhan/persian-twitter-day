import datetime
import tweepy
from celery import shared_task
from tw.views import TweetCloud
from tw_analysis.settings.local_settings import api
from tw_analysis.settings.local_settings import ADMIN_TW_ACCOUNT


@shared_task
def auto_follow_back():
    api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='i\'m going to follow back :)')
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()


@shared_task
def keep_alive():
    #
    now_time = datetime.datetime.now().strftime('%d-%b-%Y | %H:%M:%S')
    api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='i\'m here \n {}'.format(now_time))


@shared_task
def tweet_cloud(from_date=None, to_date="Today", from_time=None, to_time="Now", max_words=1000):
    command_cloud = TweetCloud()
    command_cloud.generate(from_date=from_date, to_date=to_date, from_time=from_time, to_time=to_time,
                           max_words=max_words)
    command_cloud.send()

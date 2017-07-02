import datetime
from celery import shared_task
import tweepy

from tw.views import TweetCloud
from tw_analysis.settings.local_settings import api


@shared_task
def auto_follow_back():
    api.send_direct_message(user='last_elvish', text='i\'m going to follow back :)')
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()


@shared_task
def keep_alive():
    #
    now_time = datetime.datetime.now().strftime('%d-%b-%Y | %H:%M:%S')
    api.send_direct_message(user='last_elvish', text='i\'m here \n {}'.format(now_time))


@shared_task
def tweet_cloud():
    command_cloud = TweetCloud()
    command_cloud.generate()
    command_cloud.send()

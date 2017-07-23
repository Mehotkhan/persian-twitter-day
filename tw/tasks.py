import datetime
import tweepy
from celery import shared_task
from tw.models import MessageBoot
from tw.views import TweetCloud
from tw_analysis.settings.local_settings import api
from tw_analysis.settings.local_settings import ADMIN_TW_ACCOUNT
# from multiprocessing import Pool
from billiard.pool import Pool


@shared_task
def auto_follow_back():
    api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='i\'m going to follow back :)')
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()


@shared_task()
def keep_alive():
    now_time = datetime.datetime.now().strftime('%d-%b-%Y | %H:%M:%S')
    MessageBoot.send('i\'m here \n {}'.format(now_time))


@shared_task
def tweet_cloud(from_date, from_time, max_words=1000):
    f_date = None
    f_time = None
    if from_date == 0:
        f_date = None
    else:
        f_date = float(from_date)

    if from_time == 0:
        f_time = None
    else:
        f_time = float(from_time)

    # pool = Pool(processes=4)
    TweetCloud.send_text_cloud(f_date, from_time, max_words)
    # pool.apply_async(TweetCloud.send_text_cloud, args=(f_date, from_time, max_words))
    # pool.close()
    # pool.join()

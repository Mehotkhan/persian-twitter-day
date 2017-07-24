import datetime
import tweepy
from celery import shared_task
from tw.models import MessageBoot
from tw.views import TweetCloud, TweetChart, HashtagTrend, EmojiTrend
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

    command_cloud = TweetCloud()
    MessageBoot.send('im going to generate Text CLOUD')
    command_cloud.generate(from_date=f_date, from_time=f_time,
                           max_words=max_words)
    command_cloud.send()
    MessageBoot.send('Text Cloud send')


@shared_task
def tweet_chart(from_date, from_time):
    if from_date == 0:
        from_date = None
    else:
        from_date = from_date
    if from_time == 0:
        from_time = None
    else:
        from_time = from_time

    TweetChart.send_tweet_chart(from_date, from_time)


@shared_task
def hashtags_trends(from_date, from_time):
    if from_date == 0:
        from_date = None
    else:
        from_date = from_date
    if from_time == 0:
        from_time = None
    else:
        from_time = from_time

    HashtagTrend.send_hashtags_trends(from_date, from_time)


@shared_task
def emoji_trends(from_date, from_time):
    if from_date == 0:
        from_date = None
    else:
        from_date = from_date
    if from_time == 0:
        from_time = None
    else:
        from_time = from_time

    EmojiTrend.send_data(from_date, from_time)

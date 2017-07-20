import datetime, pytz
import json
import re
import time
import sys

from mongoengine import Q

from tw_analysis.settings.base import TIME_ZONE
from tweepy import StreamListener, Stream, OAuthHandler
from tw.mongo_model import Analysis
from tw_analysis.settings.local_settings import *
from django.utils import timezone
from tw.text_cleaner import FetchText


# class FetchTweets(object):
#     @staticmethod
#     def fetch():
#         today = datetime.datetime.today().strftime('%Y-%m-%d')
#         # tweets = []
#         # tmpTweets = api.home_timeline()
#         # for tweet in tmpTweets:
#         #     if today < tweet.created_at < today:
#         #         tweets.append(tweet)
#         counter2 = 0
#         while True:
#             try:
#                 for tweet in tweepy.Cursor(api.home_timeline,
#                                            since=today, until=today).items(999999999):  # changeable here
#                     try:
#                         print("{:2d} tweets saved".format(counter2))
#                         if tweet.created_at.strftime('%Y-%m-%d') == today:
#                             print(tweet.created_at.strftime('%Y-%m-%d'))
#
#                         if tweet.text:
#                             result = db.tweet.insert_one(tweet._json)
#                             # print(line['text'])
#                             # print('tweets of {} imported'.format(tweet.user.screen_name))
#                         counter2 += 1
#                         if counter2 == 250:
#                             for i in range(20 * 60, 0, -1):
#                                 time.sleep(1)
#                                 sys.stdout.write("\r")
#                                 sys.stdout.write("{:2d} seconds remaining.".format(i))
#                                 sys.stdout.flush()
#                             continue
#                     except:
#                         print('fuck ?')
#
#             except tweepy.TweepError:
#                 print('TweepError')
#                 for i in range(20 * 60, 0, -1):
#                     time.sleep(1)
#                     sys.stdout.write("\r")
#                     sys.stdout.write("{:2d} seconds remaining.".format(i))
#                     sys.stdout.flush()
#                 continue


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        data_json = json.loads(data)
        if data_json.get('text'):
            # check dumplicate tweet
            if Analysis.objects(tweet_id=data_json['id']).count() == 0:
                tweet = Analysis()
                tweet.tweet_id = data_json['id']
                tweet.text = data_json['text']
                tweet.clean_text = FetchText.generate(data_json['text'])
                tweet.user_name = data_json['user']['name']
                tweet.user_id = data_json['user']['id']
                tweet.user_screen_name = data_json['user']['screen_name']
                tweet.user_location = data_json['user']['location']
                tweet.user_created_at = datetime.datetime.strptime(data_json['user']['created_at'],
                                                                   '%a %b %d %H:%M:%S +0000 %Y')
                tweet.user_description = data_json['user']['description']
                tweet.user_followers_count = data_json['user']['followers_count']
                tweet.user_friends_count = data_json['user']['friends_count']
                tweet.user_statuses_count = data_json['user']['statuses_count']
                tweet.user_favourites_count = data_json['user']['favourites_count']
                tweet.create_date_timestamp_ms = data_json['timestamp_ms']
                tweet.create_date = datetime.datetime.strptime(data_json['created_at'],
                                                               '%a %b %d %H:%M:%S +0000 %Y')
                tweet.source = re.findall(r'<a .*>(.*)</a>', data_json['source'])[0]
                tweet.is_quote_status = data_json['is_quote_status']
                tweet.media_type = data_json['entities']['media'] if data_json['entities'].get('media') else ''
                tweet.retweet_count = data_json['retweeted_status']['retweet_count'] if data_json.get(
                    'retweeted_status') else 0
                tweet.favorite_count = data_json['retweeted_status']['favorite_count'] if data_json.get(
                    'retweeted_status') else 0
                tweet.user_mentions = data_json['entities']['user_mentions'] if data_json['entities'].get(
                    'user_mentions') else []
                tweet.hashtags = data_json['entities']['hashtags'] if data_json['entities'].get(
                    'hashtags') else []
                tweet.save()
                # print('data saved')
            else:
                print('dump Tweet')
        else:
            pass

        return True


def on_error(self, status):
    print(status)


class FetchStream(object):
    @staticmethod
    def fetch():
        print('hello')
        l = StdOutListener()
        auth = OAuthHandler(consumer_key_data, consumer_secret_data)
        auth.set_access_token(access_token_data, access_token_secret_data)
        # stream = api.St
        stream = Stream(auth, l).userstream("with=following")


class MessageBoot(object):
    @staticmethod
    def send():
        api.send_direct_message(user='last_elvish', text='hi , im load ;)')

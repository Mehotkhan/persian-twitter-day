import datetime
import json
import time
import sys
# import tweepy
# from pymongo import MongoClient
from tweepy import StreamListener, Stream, OAuthHandler

from tw.mongo_model import Analysis
from tw_analysis.settings.local_settings import *


class FetchTweets(object):
    @staticmethod
    def fetch():
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        # tweets = []
        # tmpTweets = api.home_timeline()
        # for tweet in tmpTweets:
        #     if today < tweet.created_at < today:
        #         tweets.append(tweet)
        counter2 = 0
        while True:
            try:
                for tweet in tweepy.Cursor(api.home_timeline,
                                           since=today, until=today).items(999999999):  # changeable here
                    try:
                        print("{:2d} tweets saved".format(counter2))
                        if tweet.created_at.strftime('%Y-%m-%d') == today:
                            print(tweet.created_at.strftime('%Y-%m-%d'))

                        if tweet.text:
                            result = db.tweet.insert_one(tweet._json)
                            # print(line['text'])
                            # print('tweets of {} imported'.format(tweet.user.screen_name))
                        counter2 += 1
                        if counter2 == 250:
                            for i in range(20 * 60, 0, -1):
                                time.sleep(1)
                                sys.stdout.write("\r")
                                sys.stdout.write("{:2d} seconds remaining.".format(i))
                                sys.stdout.flush()
                            continue
                    except:
                        print('fuck ?')

            except tweepy.TweepError:
                print('TweepError')
                for i in range(20 * 60, 0, -1):
                    time.sleep(1)
                    sys.stdout.write("\r")
                    sys.stdout.write("{:2d} seconds remaining.".format(i))
                    sys.stdout.flush()
                continue


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        data_json = json.loads(data)
        if data_json.get('text'):
            tweet = Analysis()
            tweet.text = data_json['text']
            tweet.username = data_json['user']['name']
            tweet.user_id = data_json['user']['id']
            tweet.user_screen_name = data_json['user']['screen_name']
            tweet.create_date = data_json['created_at']
            tweet.create_date = datetime.datetime.strptime(data_json['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            tweet.save()
            print('data saved')
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

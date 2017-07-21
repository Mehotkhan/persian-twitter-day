import datetime
import json
import re
import threading
from http.client import IncompleteRead
from tweepy import StreamListener, Stream, OAuthHandler
from tw.mongo_model import Analysis
from tw_analysis.settings.local_settings import *
from tw.text_cleaner import FetchText
import queue


class PersianListener(StreamListener):
    def __init__(self):
        super(StreamListener, self).__init__()
        self.input_queue = queue.Queue()
        self.stop_event = threading.Event()

    def on_data(self, data):
        data_json = json.loads(data)
        # print("Starting data collection thread...")
        d = threading.Thread(target=self.save_tweet, args=(data_json, self.input_queue, self.stop_event))
        d.start()
        # print("Done.")

        return True

    def on_error(self, status):
        print(status)

    @staticmethod
    def save_tweet(data_json, input_queue, stop_event):
        while not stop_event.is_set():
            if data_json.get('text'):
                # check if tweet is retweet:
                if data_json.get('retweeted_status'):
                    retweeted_id = data_json['retweeted_status']['id']
                    tw_object = Analysis.objects(tweet_id=retweeted_id)
                    # if not exist
                    if tw_object.count() == 0 and not data_json['retweeted_status']['entities'].get('user_mentions'):
                        tweet = Analysis()
                        tweet.tweet_id = retweeted_id
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
                        tweet.retweet_count = data_json['retweeted_status']['retweet_count']
                        tweet.favorite_count = data_json['retweeted_status']['favorite_count']
                        # tweet.user_mentions = data_json['entities']['user_mentions'] if data_json['entities'].get(
                        #     'user_mentions') else []
                        tweet.hashtags = data_json['entities']['hashtags'] if data_json['entities'].get(
                            'hashtags') else []
                        tweet.save()
                        print('retweet saved')
                        input_queue.put(None)
                        return
                    # if not exist
                    elif data_json['retweeted_status']['entities'].get('user_mentions'):
                        tweet = Analysis()
                        tweet.tweet_id = retweeted_id
                        tweet.text = data_json['text']
                        # tweet.clean_text = FetchText.generate(data_json['text'])
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
                        tweet.retweet_count = data_json['retweeted_status']['retweet_count']
                        tweet.favorite_count = data_json['retweeted_status']['favorite_count']
                        tweet.user_mentions = data_json['entities']['user_mentions'] if data_json['entities'].get(
                            'user_mentions') else []
                        tweet.hashtags = data_json['entities']['hashtags'] if data_json['entities'].get(
                            'hashtags') else []
                        tweet.save()
                        print('retweet[\'mention\']  saved')
                        input_queue.put(None)
                        return
                    else:
                        # tw_object.retweet_count = data_json['retweeted_status']['retweet_count']
                        # tw_object.favorite_count = data_json['retweeted_status']['favorite_count']
                        tw_object.update(retweet_count=data_json['retweeted_status']['retweet_count'],
                                         favorite_count=data_json['retweeted_status']['favorite_count'])
                        print('retweet  updated')
                        input_queue.put(None)
                        return
                # save if not retweeted and not mention
                elif not data_json['entities'].get('user_mentions') and Analysis.objects(
                        tweet_id=data_json['id']).count() == 0:
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
                    print('tweet saved')
                    input_queue.put(None)
                    return
                # if tweet is mention
                elif data_json['entities'].get('user_mentions') and Analysis.objects(
                        tweet_id=data_json['id']).count() == 0:
                    tweet = Analysis()
                    tweet.tweet_id = data_json['id']
                    tweet.text = data_json['text']
                    # tweet.clean_text = FetchText.generate(data_json['text'])
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
                    print('tweet[\'mention\'] saved')
                    input_queue.put(None)
                    return
                elif Analysis.objects(
                        tweet_id=data_json['id']).count() > 0:
                    print('dump Tweet')
                    input_queue.put(None)
                    return
                else:
                    print('some data not in loop ?')

            else:
                input_queue.put(None)
                return

        print("Terminating data collection...")
        input_queue.put(None)
        return


class FetchStream(object):
    @staticmethod
    def fetch():
        print('hello')
        while True:
            try:
                l = PersianListener()
                auth = OAuthHandler(consumer_key_data, consumer_secret_data)
                auth.set_access_token(access_token_data, access_token_secret_data)
                # stream = api.St
                stream = Stream(auth, l).userstream("with=following")
            except IncompleteRead:
                # Oh well, reconnect and keep trucking
                continue
            except KeyboardInterrupt:
                # Or however you want to exit this loop
                stream.disconnect()
                break


class MessageBoot(object):
    @staticmethod
    def send():
        api.send_direct_message(user='last_elvish', text='hi , im load ;)')

import datetime
import re
from collections import Counter

import jdatetime
import pygal
from mongoengine import Q
import emoji
from tw.models import MessageBoot
from tw.mongo_model import Analysis
from tw_analysis.settings.local_settings import api
from persian_wordcloud.wordcloud import PersianWordCloud, add_stop_words
from os import path
from PIL import Image
import numpy as np
from dateutil import tz


class TweetChart(object):
    def __init__(self):
        self.file_names = []
        self.d = path.dirname(__file__)
        self.all_tweets_count = None
        self.from_date = None
        self.from_time = None
        self.to_date = None
        self.date_list = []

    def generate(self, from_date=None, to_date="Today", from_time=None, to_time="Now"):
        if from_time:
            self.from_time = abs(from_time)
        if from_date:
            self.from_date = abs(from_date)
        if from_date and to_date:
            if from_date == to_date and from_date == "Today":
                # Read the whole text.
                self.to_date = datetime.date.today()
                self.date_list = [(self.to_date - datetime.timedelta(x)) for x in range(-24, 2)]
            elif isinstance(from_date, int) and to_date == "Today":
                self.to_date = datetime.date.today()
                self.date_list = [(self.to_date + datetime.timedelta(x)) for x in range(from_date, 2)]
        if from_time and to_time:
            if isinstance(from_time, int) and to_time == "Now":
                self.to_date = datetime.datetime.now().replace(tzinfo=tz.tzlocal())
                self.date_list = [(self.to_date + datetime.timedelta(hours=x)).replace(tzinfo=tz.tzlocal()) for x in
                                  range(from_time, 2)]
        tw_count = []
        quotes_count = []
        retweet_count = []
        all_tweet_count = []
        all_mention_count = []
        all_media_count = []
        for index, item in enumerate(self.date_list):
            if index == len(self.date_list) - 1:
                break
            tweets = Analysis.objects(
                Q(create_date__gte=self.date_list[index])
                &
                Q(create_date__lt=self.date_list[index + 1])
                &
                Q(retweet_count=0)

            ).all()
            tw_count.append(tweets.count())
            # count quotes
            quotes = Analysis.objects(
                Q(create_date__gte=self.date_list[index])
                &
                Q(create_date__lt=self.date_list[index + 1])
                &
                Q(is_quote_status=True)

            ).all()
            quotes_count.append(quotes.count())
            # count retweet
            retweet = Analysis.objects(
                Q(create_date__gte=self.date_list[index])
                &
                Q(create_date__lt=self.date_list[index + 1])
                &
                Q(retweet_count__gt=0)

            ).all()
            retweet_count.append(retweet.count())
            # user mention #
            all_mention = Analysis.objects(
                Q(create_date__gte=self.date_list[index])
                &
                Q(create_date__lt=self.date_list[index + 1])
                &
                Q(user_mentions__ne=[])

            ).all()
            all_mention_count.append(all_mention.count())
            # Media
            all_media = Analysis.objects(
                Q(create_date__gte=self.date_list[index])
                &
                Q(create_date__lt=self.date_list[index + 1])
                &
                Q(media_type__ne='')

            ).all()
            all_media_count.append(all_media.count())
            # all tweet
            all_tweet = Analysis.objects(
                Q(create_date__gte=self.date_list[index])
                &
                Q(create_date__lt=self.date_list[index + 1])

            ).all()
            all_tweet_count.append(all_tweet.count())

        date_chart = pygal.Bar(margin=100, height=1000, width=1000, x_label_rotation=90)
        date_chart.x_labels = map(
            lambda d: jdatetime.datetime.fromgregorian(datetime=d).strftime(
                '%m/%d - %H:%m ') if isinstance(d, datetime.datetime) else jdatetime.date.fromgregorian(
                date=d).strftime(
                '%a %m/%d'),
            self.date_list[:-1])
        date_chart.title = 'Count  of ALL'
        date_chart.add("all_tweet_count", all_tweet_count)
        date_chart.add("tw", tw_count)
        date_chart.add("retweet", retweet_count)
        date_chart.add("quotes", quotes_count)
        date_chart.add("mention", all_mention_count)
        date_chart.add("all_media", all_media_count)

        # # create pie chart
        self.all_tweets_count = sum(all_tweet_count)
        pie_chart = pygal.Pie(inner_radius=.4)
        pie_chart.title = 'From All  - More than 100% - {} tweet'.format(self.all_tweets_count)
        pie_chart.add('tw {0:.2f} %'.format(100 * sum(tw_count) / self.all_tweets_count),
                      100 * float(sum(tw_count)) / float(self.all_tweets_count))

        pie_chart.add('quotes {0:.2f} %'.format(100 * sum(quotes_count) / self.all_tweets_count),
                      100 * float(sum(quotes_count)) / float(self.all_tweets_count))

        pie_chart.add('retweet {0:.2f} %'.format(100 * sum(retweet_count) / self.all_tweets_count),
                      100 * float(sum(retweet_count)) / float(self.all_tweets_count))

        pie_chart.add('mention {0:.2f} %'.format(100 * sum(all_mention_count) / self.all_tweets_count),
                      100 * float(sum(all_mention_count)) / float(self.all_tweets_count))
        pie_chart.add('media {0:.2f} %'.format(100 * sum(all_media_count) / self.all_tweets_count),
                      100 * float(sum(all_media_count)) / float(self.all_tweets_count))

        # create file
        filename = datetime.datetime.today().strftime('%Y-%m-%d-%H:%m')
        date_chart.render_to_png(path.join(self.d, 'tmp/' + filename + '-chart.png'), dpi=600)
        self.file_names.append(path.join(self.d, 'tmp/' + filename + '-chart.png'))
        pie_chart.render_to_png(path.join(self.d, 'tmp/' + filename + '-pie-chart.png'), dpi=300)
        self.file_names.append(path.join(self.d, 'tmp/' + filename + '-pie-chart.png'))

    def send(self):

        media_ids = []
        for file in self.file_names:
            res = api.media_upload(file)
            media_ids.append(res.media_id)
        status_text = ''
        if self.from_time:
            status_text = "چارت توییت های {} ساعت گذشته از {} توییت ".format(
                self.from_time,
                self.all_tweets_count,
            )
        if self.from_date:
            status_text = "چارت توییت های {} روز گذشته از {} توییت ".format(
                int(self.from_time),
                self.all_tweets_count,
            )
        api.update_status(status=status_text, media_ids=media_ids)

    @staticmethod
    def send_tweet_chart(f_date, f_time):
        command_cloud = TweetChart()
        MessageBoot.send('im going to generate tweet chart')
        command_cloud.generate(from_date=f_date, from_time=f_time)
        command_cloud.send()
        MessageBoot.send('tweet chart Cloud send')


class TweetCloud(object):
    def __init__(self):
        self.tweet_cloud = None
        self.file_names = []
        self.d = path.dirname(__file__)
        self.all_tweets_count = None
        self.from_date = None
        self.from_time = None
        self.to_date = None

    def generate(self, from_date=None, to_date="Today", from_time=None, to_time="Now", max_words=1000):
        self.from_time = abs(from_time)
        if from_date and to_date:
            if from_date == to_date and from_date == "Today":
                # Read the whole text.
                self.from_date = datetime.date.today() - datetime.timedelta(1)
                self.to_date = datetime.date.today()
            elif isinstance(from_date, float) and to_date == "Today":
                self.from_date = datetime.date.today() + datetime.timedelta(from_date)
                self.to_date = datetime.date.today()
        if from_time and to_time:
            if isinstance(from_time, float) and to_time == "Now":
                self.from_date = datetime.datetime.now() + datetime.timedelta(hours=from_time)
                self.to_date = datetime.datetime.now()
        all_tweets = Analysis.objects(
            Q(create_date__lt=self.to_date.replace(tzinfo=tz.tzlocal()))
            &
            Q(create_date__gte=self.from_date.replace(tzinfo=tz.tzlocal()))
            &
            Q(user_mentions=[])

        ).all()
        self.all_tweets_count = len(all_tweets)
        all_words = []
        for item in all_tweets:
            tw_text = item.clean_text
            for sentese in tw_text:
                for item, key in sentese:
                    if key in ['Ne', 'N', 'AJ', 'AJe']:
                        word = ''
                        for w in item:
                            if u'\u0600' <= w <= u'\u06FF':
                                word += w
                        all_words.append(word)

        text = ' '.join(all_words)
        twitter_mask = np.array(Image.open(path.join(self.d, "image/twitter-logo.jpg")))
        # Generate a word cloud image
        stopwords = add_stop_words(['توییت', 'توییتر'])
        self.tweet_cloud = PersianWordCloud(
            only_persian=True,
            max_words=max_words,
            stopwords=stopwords,
            margin=0,
            min_font_size=10,
            max_font_size=80,
            random_state=1,
            background_color="white",
            mask=twitter_mask
        ).generate(text)

    def send(self):
        filename = datetime.datetime.today().strftime('%Y-%m-%d-%H:%m')
        image = (path.join(self.d, 'tmp/' + filename + '.png'))
        img = self.tweet_cloud.to_image()
        img.save(image)
        # img.show()
        self.file_names.append(path.join(self.d, 'tmp/' + filename + '.png'))
        media_ids = []
        for file in self.file_names:
            res = api.media_upload(file)
            media_ids.append(res.media_id)
        status_text = "ابر کلمات {} ساعت گذشته از {} توییت".format(
            int(self.from_time),
            self.all_tweets_count,
        )
        api.update_status(status=status_text, media_ids=media_ids)

    @staticmethod
    def send_text_cloud(f_date, f_time, max_words):
        command_cloud = TweetCloud()
        MessageBoot.send('im going to generate Text CLOUD')
        command_cloud.generate(from_date=f_date, from_time=f_time,
                               max_words=max_words)
        command_cloud.send()
        MessageBoot.send('Text Cloud send')


class HashtagTrend(object):
    def __init__(self):
        self.file_names = []
        self.d = path.dirname(__file__)
        self.all_tweets_count = None
        self.from_date = None
        self.from_time = None
        self.to_date = None
        self.f_time = None
        self.hashtags = None

    def generate(self, from_date=None, to_date="Today", from_time=None, to_time="Now", hashtag_count=10):
        if from_time:
            self.f_time = abs(from_time)
        # if from_date:
        #     self.from_date = abs(from_date)
        if from_date and to_date:
            if from_date == to_date and from_date == "Today":
                # Read the whole text.
                self.from_date = datetime.date.today() - datetime.timedelta(1)
                self.to_date = datetime.date.today()
            elif isinstance(from_date, int) and to_date == "Today":
                self.from_date = datetime.date.today() + datetime.timedelta(from_date)
                self.to_date = datetime.date.today()
        if from_time and to_time:
            if isinstance(from_time, int) and to_time == "Now":
                self.from_date = datetime.datetime.now() + datetime.timedelta(hours=from_time)
                self.to_date = datetime.datetime.now()
        all_tweets = Analysis.objects(
            Q(create_date__lt=self.to_date.replace(tzinfo=tz.tzlocal()))
            &
            Q(create_date__gte=self.from_date.replace(tzinfo=tz.tzlocal()))
            &
            Q(hashtags__ne=[])

        ).all()
        self.all_tweets_count = len(all_tweets)
        all_hashtags = []
        for item in all_tweets:
            for hashtag in item.hashtags:
                all_hashtags.append(self.remove_ar(hashtag['text']))
        count_all = Counter()
        count_all.update(all_hashtags)
        self.hashtags = count_all.most_common(hashtag_count)

    def send(self):
        status_text = 'هشتگ های داغِ {} ساعت گذشته:'.format(int(self.f_time))
        for name, count in self.hashtags:
            new_hashtag = '\n#' + name
            if len(status_text) + len(new_hashtag) < 140:
                status_text += new_hashtag
        api.update_status(status=status_text)

    @staticmethod
    def remove_ar(text):
        dic = {
            'ك': 'ک',
            'دِ': 'د',
            'بِ': 'ب',
            'زِ': 'ز',
            'ذِ': 'ذ',
            'شِ': 'ش',
            'سِ': 'س',
            'ى': 'ی',
            'ي': 'ی'
        }
        pattern = "|".join(map(re.escape, dic.keys()))
        return re.sub(pattern, lambda m: dic[m.group()], text)

    @staticmethod
    def send_hashtags_trends(f_date, f_time):
        command_cloud = HashtagTrend()
        MessageBoot.send('im going to generate Hashtags trends')
        command_cloud.generate(from_date=f_date, from_time=f_time, hashtag_count=15)
        command_cloud.send()
        MessageBoot.send('Hashtags trends send')


class EmojiTrend(object):
    def __init__(self):
        self.file_names = []
        self.d = path.dirname(__file__)
        self.all_tweets_count = None
        self.from_date = None
        self.from_time = None
        self.to_date = None
        self.f_time = None
        self.emoji = None

    def generate(self, from_date=None, to_date="Today", from_time=None, to_time="Now", emoji_count=10):
        if from_time:
            self.f_time = abs(from_time)
        # if from_date:
        #     self.from_date = abs(from_date)
        if from_date and to_date:
            if from_date == to_date and from_date == "Today":
                # Read the whole text.
                self.from_date = datetime.date.today() - datetime.timedelta(1)
                self.to_date = datetime.date.today()
            elif isinstance(from_date, int) and to_date == "Today":
                self.from_date = datetime.date.today() + datetime.timedelta(from_date)
                self.to_date = datetime.date.today()
        if from_time and to_time:
            if isinstance(from_time, int) and to_time == "Now":
                self.from_date = datetime.datetime.now() + datetime.timedelta(hours=from_time)
                self.to_date = datetime.datetime.now()
        all_tweets = Analysis.objects(
            Q(create_date__lt=self.to_date.replace(tzinfo=tz.tzlocal()))
            &
            Q(create_date__gte=self.from_date.replace(tzinfo=tz.tzlocal()))
            &
            Q(hashtags__ne=[])

        ).all()
        self.all_tweets_count = len(all_tweets)
        all_emoji = []
        for item in all_tweets:
            all_emoji += (c for c in item.text if c in emoji.UNICODE_EMOJI)
        count_all = Counter()
        count_all.update(all_emoji)
        self.emoji = count_all.most_common(emoji_count)

    def send(self):
        status_text = 'ایموجی های داغِ {} ساعت گذشته:'.format(int(self.f_time))
        for name, count in self.emoji:
            new_emoji = '\n' + name
            if len(status_text) + len(new_emoji) < 140:
                status_text += new_emoji
        print(status_text)
        exit()
        api.update_status(status=status_text)

    @staticmethod
    def send_data(f_date, f_time):
        command_cloud = EmojiTrend()
        # MessageBoot.send('im going to generate emoji trends')
        command_cloud.generate(from_date=f_date, from_time=f_time, emoji_count=8)
        command_cloud.send()
        # MessageBoot.send('emoji trends send')

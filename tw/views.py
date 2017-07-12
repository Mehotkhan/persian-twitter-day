import datetime
import jdatetime
from mongoengine import Q
from tw.mongo_model import Analysis
from tw_analysis.settings.local_settings import api, ADMIN_TW_ACCOUNT
from persian_wordcloud.wordcloud import STOPWORDS, PersianWordCloud
from os import path
from PIL import Image
import numpy as np
from dateutil import tz


class TweetCloud(object):
    def __init__(self):
        self.tweet_cloud = None
        self.file_names = []
        self.d = path.dirname(__file__)
        self.all_tweets_count = None
        self.from_date = None
        self.to_date = None

    @staticmethod
    def is_perisan(s):
        return u'\u0600' <= s <= u'\u06FF'

    def generate(self, from_date=None, to_date="Today", from_time=None, to_time="Now", max_words=1000):
        api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='hey , i\'m going to generate text CLOUD :*')
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

        ).all()
        self.all_tweets_count = len(all_tweets)
        all_words = []
        for item in all_tweets:
            tw_text = item.text.split()
            for w in tw_text:
                if self.is_perisan(w):
                    words = ''
                    words += ' ' + w
                    all_words.append(words)

        text = ''.join(all_words)
        twitter_mask = np.array(Image.open(path.join(self.d, "image/twitter-logo.jpg")))
        # Generate a word cloud image
        STOPWORDS.add('می')
        stopwords = set(STOPWORDS)
        self.tweet_cloud = PersianWordCloud(
            only_persian=True,
            max_words=max_words,
            stopwords=stopwords,
            margin=0,
            # width=800,
            # height=800,
            min_font_size=10,
            max_font_size=100,
            random_state=1,
            background_color="white",
            mask=twitter_mask
        ).generate(text)

    def send(self):
        api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='hey , i\'m going to send text CLOUD :*')
        filename = datetime.datetime.today().strftime('%Y-%m-%d-%H:%m')
        image = (path.join(self.d, 'tmp/' + filename + '.png'))
        img = self.tweet_cloud.to_image()
        img.save(image)
        self.file_names.append(path.join(self.d, 'tmp/' + filename + '.png'))
        media_ids = []
        for file in self.file_names:
            res = api.media_upload(file)
            media_ids.append(res.media_id)
        from_date = self.from_date.replace(tzinfo=tz.tzlocal())
        to_date = self.to_date.replace(tzinfo=tz.tzlocal())
        j_from_date = jdatetime.datetime.fromgregorian(datetime=from_date)
        j_to_date = jdatetime.datetime.fromgregorian(datetime=to_date)
        status_text = "ابر کلمات تولید شده از {} تویت از تاریخ {} تا تاریخ {}".format(
            self.all_tweets_count,
            j_from_date.strftime(
                " %H:%m - %Y/%m/%d"),
            j_to_date.strftime(
                " %H:%m - %Y/%m/%d")
        )
        api.update_status(status=status_text, media_ids=media_ids)
        api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='hora , text cloud image sends :**')

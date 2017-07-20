import datetime
import jdatetime
from mongoengine import Q
from tw.mongo_model import Analysis
from tw_analysis.settings.local_settings import api, ADMIN_TW_ACCOUNT
from persian_wordcloud.wordcloud import STOPWORDS, PersianWordCloud, add_stop_words
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
        self.from_time = None
        self.to_date = None

    def generate(self, from_date=None, to_date="Today", from_time=None, to_time="Now", max_words=1000):
        self.from_time = abs(from_time)
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
            tw_text = item.clean_text
            for sentese in tw_text:
                for item, key in sentese:
                    if key in ['Ne', 'N', 'AJ', 'AJe']:
                        all_words.append(item)

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
        # api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='hey , i\'m going to send text CLOUD :*')
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
            self.from_time,
            self.all_tweets_count,
        )
        api.update_status(status=status_text, media_ids=media_ids)
        api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='text cloud image sends :**')

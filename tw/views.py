import datetime
import jdatetime
from mongoengine import Q
from tw.mongo_model import Analysis
from tw_analysis.settings.local_settings import api, ADMIN_TW_ACCOUNT
from os import path
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display


class TweetCloud(object):
    def __init__(self):
        self.tweet_cloud = None
        self.file_names = []
        self.d = path.dirname(__file__)
        self.all_tweets_count = None
        self.font_path = path.join(self.d, 'fonts', 'Vazir-Light.ttf')
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
            elif isinstance(float, from_date) and to_date == "Today":
                self.from_date = datetime.date.today() + datetime.timedelta(from_date)
                self.to_date = datetime.date.today()
        if from_time and to_time:
            if isinstance(float, from_time) and to_time == "Now":
                self.from_date = datetime.datetime.now() + datetime.timedelta(hours=from_time)
                self.to_date = datetime.datetime.now()

        all_tweets = Analysis.objects(
            Q(create_date__lt=self.to_date)
            &
            Q(create_date__gte=self.from_date)

        ).all()
        self.all_tweets_count = len(all_tweets)
        all_words = []
        words = ''
        for item in all_tweets:
            text = item.text.split()
            for w in text:
                if self.is_perisan(w):
                    words += ' ' + w
            try:
                text_ = arabic_reshaper.reshape(words)
                bidi_text = get_display(text_)
                all_words.append(bidi_text)
            except AssertionError:
                exit()

        text = ''.join(all_words)
        stopwords = set([get_display(arabic_reshaper.reshape(x.strip())) for x in
                         open((path.join(self.d, 'stop_words.txt')), encoding='utf-8').read().split('\n')])

        self.tweet_cloud = WordCloud(
            font_path=self.font_path,
            max_words=max_words,
            stopwords=stopwords,
            # mask=mask,
            margin=0,
            width=800,
            height=800,
            min_font_size=1,
            max_font_size=500,
            background_color="black",
            random_state=1
        ).generate(text)

    def send(self):
        api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='hey , i\'m going to send text CLOUD :*')
        # The pil way (if you don't have matplotlib)
        filename = datetime.datetime.today().strftime('%Y-%m-%d')
        image = (path.join(self.d, filename + '.png'))
        img = self.tweet_cloud.to_image()
        img.save(image)
        self.file_names.append(path.join(self.d, filename + '.png'))
        media_ids = []
        for file in self.file_names:
            res = api.media_upload(file)
            media_ids.append(res.media_id)
        yesterday = datetime.date.today() - datetime.timedelta(1)
        date = jdatetime.date.fromgregorian(date=yesterday)
        status_text = "ابر کلمات از {} تویت در تاریخ {}".format(50,
                                                                date.strftime(
                                                                    "%d-%b-%Y "))
        api.update_status(status=status_text, media_ids=media_ids)
        api.send_direct_message(user=ADMIN_TW_ACCOUNT, text='hora , text cloud image sends :**')

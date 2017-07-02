import datetime
import jdatetime
from mongoengine import Q
from tw.mongo_model import Analysis
from tw_analysis.settings.local_settings import api
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

    @staticmethod
    def is_perisan(s):
        return u'\u0600' <= s <= u'\u06FF'

    def generate(self):
        api.send_direct_message(user='last_elvish', text='hey , i\'m going to generate text CLOUD :*')
        font_path = path.join(self.d, 'fonts', 'Vazir-Light.ttf')
        # Read the whole text.
        yesterday = datetime.date.today() - datetime.timedelta(1)
        tomorow = datetime.date.today() + datetime.timedelta(1)
        today = datetime.date.today()
        all_tweets = Analysis.objects(
            Q(create_date__lt=today)
            &
            Q(create_date__gte=yesterday)

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
            font_path=font_path,
            max_words=1000,
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
        api.send_direct_message(user='last_elvish', text='hey , i\'m going to send text CLOUD :*')
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
        api.send_direct_message(user='last_elvish', text='hora , text cloud image sends :**')

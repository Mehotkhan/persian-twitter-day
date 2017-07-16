from __future__ import unicode_literals
from hazm import *
from os import path


class FetchText(object):
    @staticmethod
    def clean_text(text):
        all_words = []
        text = text.split()
        for words in text:
            if u'\u0600' <= words <= u'\u06FF':
                all_words.append(words)
        return ' '.join(all_words)

    @classmethod
    def generate(cls, text):
        # first we split sentence of tweet
        sentences = sent_tokenize(text)
        # now find every section of sentence
        text_data = []
        for sentence in sentences:
            normalizer = Normalizer()
            clean_sentence = cls.clean_text(text=sentence)
            text_normal = normalizer.normalize(clean_sentence)
            tagger = POSTagger(model=path.dirname(__file__) + '/resources/postagger.model')
            taged = tagger.tag(word_tokenize(text_normal))
            text_data.append(taged)
            # for item, key in taged:
            #     if key in ['Ne', 'N', 'AJ', 'AJe']:
            #         text_data.append(item)
        return text_data

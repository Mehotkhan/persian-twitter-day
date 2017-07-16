from __future__ import unicode_literals
from hazm import *
from os import path


class FetchText(object):
    @staticmethod
    def generate(text):
        # first we split sentence of tweet
        sentences = sent_tokenize(text)
        # now find every section of sentence
        text_data = []
        for sentence in sentences:
            normalizer = Normalizer()
            text_normal = normalizer.normalize(sentence)
            tagger = POSTagger(model=path.dirname(__file__) + '/resources/postagger.model')
            taged = tagger.tag(word_tokenize(text_normal))
            text_data.append(taged)
            # for item, key in taged:
            #     if key in ['Ne', 'N', 'AJ', 'AJe']:
            #         text_data.append(item)
        return text_data

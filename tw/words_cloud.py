#!/usr/bin/env python
"""
Minimal Example
===============

Generating a square wordcloud from the US constitution using default arguments.
"""
import numpy as np
import string
from PIL import Image
from os import path
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display

# from wordcloud import WordCloud, STOPWORDS



d = path.dirname(__file__)
mask = np.array(Image.open(path.join(d, "stormtrooper_mask.png")))
font_path = path.join(d, 'management/commands/fonts', 'Vazir-Light.ttf')
# Read the whole text.

text = open(path.join(d, 'persian.txt'), encoding='utf-8').read()

text_ = arabic_reshaper.reshape(text)
bidi_text = get_display(text_)
# Generate a word cloud image


STOPWORDS = set([get_display(arabic_reshaper.reshape(x.strip())) for x in
                 open((path.join(d, 'management/commands/stop_words.txt')), encoding='utf-8').read().split('\n')])
# STOPWORDS = arabic_reshaper.reshape(STOPWORDS)
# bidi_text_stop = get_display(STOPWORDS)
stopwords = set(STOPWORDS)
# print(stopwords)
# exit()
wordcloud = WordCloud(
    font_path=font_path,
    max_words=5000000,
    stopwords=stopwords,
    # mask=mask,
    margin=0,
    width=800,
    height=800,
    min_font_size=1,
    max_font_size=500,
    background_color="white"
    # random_state=1
).generate(bidi_text)

# The pil way (if you don't have matplotlib)
image = wordcloud.to_image()
image.show()

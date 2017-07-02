from __future__ import unicode_literals
from hazm import *

# normalizer = Normalizer()
# normalizer.normalize('اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند')
# 'اصلاح نویسه‌ها و استفاده از نیم‌فاصله پردازش را آسان می‌کند'
#
# sent_tokenize('ما هم برای وصل کردن آمدیم! ولی برای پردازش، جدا بهتر نیست؟')
#
# word_tokenize('ولی برای پردازش، جدا بهتر نیست؟')
#
#
# stemmer = Stemmer()
# stemmer.stem('کتاب‌ها')
#
# lemmatizer = Lemmatizer()
# lemmatizer.lemmatize('می‌روم')
text = 'احساس پوچي عجيبي مرا فرا گرفته'

tagger = POSTagger(model='resources/postagger.model')
dict_ = dict(tagger.tag(word_tokenize(text)))
print(dict_)

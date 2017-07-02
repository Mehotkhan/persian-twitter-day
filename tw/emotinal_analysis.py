# from typing import Text

from polyglot.downloader import downloader
from polyglot.text import Text, Word
import arabic_reshaper
from bidi.algorithm import get_display

# print(downloader.supported_languages_table("sentiment2", 3))

# text = Text("The movie was really good.")
blob = """"آمریکا و چین در عالیترین سطح امنیتی، درباره چه موضوعاتی مذاکره می‌کنند."""

print("{:<16}{}".format("Word", "Polarity") + "\n" + "-" * 30)
# for w in text.words:
#     text_ = arabic_reshaper.reshape(w)
#     bidi_text = get_display(text_)
#     print("{:<16}{:>2}".format(bidi_text, w.polarity))
# blob = """The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world"."""
text = Text(blob)
for sent in text.sentences:
    print(sent, "\n")
    for entity in sent.entities:
        print(entity.tag, entity)

first_sentence = text.sentences[0]
first_entity = first_sentence.entities[0]
# print(first_entity)
# # print(first_entity.positive_sentiment)
# # print(first_entity.negative_sentiment)
for w in first_sentence.entities:
    # text_ = arabic_reshaper.reshape(w)
    # bidi_text = get_display(text_)
    print("{} :  positive: {:<2} | negative: {:>2}".format(w, str(w.positive_sentiment), str(w.negative_sentiment)))
    # print('{} - {} = {}'.format(w, w.positive_sentiment, w.negative_sentiment))
    # print(w.negative_sentiment)

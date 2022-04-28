# only first time
import nltk
nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer
import re
import pickle
from emot.emo_unicode import UNICODE_EMOJI, EMOTICONS_EMO


def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text.replace("_"," ")

sia = SentimentIntensityAnalyzer()
text = '''
Hilarious 😂. The feeling of making a sale 😎, The feeling of actually fulfilling orders 😒
'''
text1 = convert_emojis(text)
print(text1)
res = sia.polarity_scores(text)
print(res)
print(text1)
res1 = sia.polarity_scores(text1)

print(res1)
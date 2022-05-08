import tweepy
from emot.emo_unicode import UNICODE_EMOJI
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Tweet API Streaming
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHFbAEAAAAA0oBVG5orLLErnyAqw2po3fOae5w%3D4lgZWoMOyGG496F2aNACoKOdDCaDnxqret6oFPLToE244O6Tx6"
client = tweepy.Client(BEARER_TOKEN)


result = client.search_recent_tweets("Election Melbourne", max_results=100, next_token = "b26v89c19zqg8o3fpywln073kjkhbz4nsyrhn7dk9ea9p")
print(result)


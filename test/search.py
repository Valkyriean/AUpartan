import tweepy
from app import couch
from emot.emo_unicode import UNICODE_EMOJI
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Convert emojis to string for furter usage such as sentimental analysis with nlp package
def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text.replace("_"," ")

# Tweet API Streaming
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHFbAEAAAAA0oBVG5orLLErnyAqw2po3fOae5w%3D4lgZWoMOyGG496F2aNACoKOdDCaDnxqret6oFPLToE244O6Tx6"
client = tweepy.Client(BEARER_TOKEN)

# Collect keyword / city from Gateway
input_city = ["Canberra"]
input_keyword = "Election"

rawdb_name = "search_" + input_keyword
try:
    dbcity = couch[rawdb_name]
except:
    dbcity = couch.create(rawdb_name)

# Construct query keyword string
query_rule = input_keyword + " ("
for i in range(len(input_city)):
    if (i >= len(input_city) - 1):
        query_rule += input_city[i]
    else:
        query_rule += input_city[i]
        query_rule += " OR "
query_rule += ")"


result_finish = True
state_start = True
while result_finish:
    try:
        if (state_start):
            result = client.search_recent_tweets(query_rule, max_results = 100)
            print(result)
            if "next_token" in result[3]:
                state_start = False
                next_page = result[3]["next_token"]
            else:
                break
        else:
            result = client.search_recent_tweets(query_rule, max_results = 100, next_token = next_page)
            print(result)
            if "next_token" in result[3]:
                next_page = result[3]["next_token"]
            else:
                break
    except Exception as e:
        pass


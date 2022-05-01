from tweepy import StreamingClient, Tweet, StreamRule
import tweepy
from tokenize import group
import tweepy
import re
from flask import Blueprint,request
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, ListField, FloatField
from couchdb.design import ViewDefinition
from flaskext.couchdb import Row
from emot.emo_unicode import UNICODE_EMOJI

bp = Blueprint("politics", __name__, url_prefix="/politics")

if db_enable:
    try:
        db = couch['election']
    except:
        db = couch.create('election')

manager = CouchDBManager()

class Election(Document):
    doc_type = 'Election'
    _id = TextField()
    city = TextField()
    topic = TextField()
    tweet_text = TextField()
    tweet_emo = ListField(FloatField())

manager.add_document(Election)

englishRate = ViewDefinition('Election', 'enRate', '''\
    function(doc){
        if (doc.lang_type == 'en'){
            emit(doc.city_name, 1);
        }else{
            emit(doc.city_name, 0);
        }
    }''','''function(keys, values, rereduce){
              return (sum(values) / values.length);
    }
    ''', wrapper = Row, group = True)

# Tweet API Streaming
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHFbAEAAAAA0oBVG5orLLErnyAqw2po3fOae5w%3D4lgZWoMOyGG496F2aNACoKOdDCaDnxqret6oFPLToE244O6Tx6"
CONSUMER_KEY = "K4leUSXBdJwHytayPXdFzEzJN"
CONSUMER_SECRET = "bpyL6MhIsNKRoWDrHj0ou9wHwib7tCm4ob5p3SZam51iDZyqv4"
bearer_token = BEARER_TOKEN
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Install vader_lexicon for sentimental analysis of historic data
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# Set up NLP analysis tools
sia = SentimentIntensityAnalyzer()

def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text.replace("_"," ")

#@bp.route('/Sydney/', endpoint='Sydney', methods=["POST", "GET"])
#@bp.route('/Melbourne/', endpoint='Melbourne', methods=["POST", "GET"])
@bp.route("/<city_name>/<input_text>/")
def citylang(city_name, input_text):
    city = city_name
    follower_limit = 3000
    

    class TweetListener(StreamingClient):

        def on_tweet(self, tweet: Tweet):
            text = api.get_status(tweet.id, tweet_mode = "extended")
            if ((text.user.followers_count < follower_limit) and (text.lang != "und")):
                text = convert_emojis(text.full_text)
                text = re.sub('http://\S+|https://\S+', '', text)
                nlp_result = [sia.polarity_scores(text)["neg"], sia.polarity_scores(text)["pos"], sia.polarity_scores(text)["compound"]]

                if str(tweet.id) not in db:
                    new_historic = Election(_id = str(tweet.id), city = city_name, topic = input_text, tweet_text = text, tweet_emo = nlp_result)
                    new_historic.store(db)
                
        def on_request_error(self, status_code):
            print(status_code)
            
        def on_connection_error(self):
            self.disconnect
                
    client = TweetListener(bearer_token)
    keywords = input_text
    rules = [
        StreamRule(value = keywords, tag = city)
        # StreamRule(value=""),
        # StreamRule(value="bounding_box:[144.3896 -38.5084 145.5459 -37.3127]")
    ]

    resp = client.get_rules()
    if resp and resp.data:
        rule_ids = []
        for rule in resp.data:
            rule_ids.append(rule.id)
        client.delete_rules(rule_ids)
            
    resp = client.add_rules(rules, dry_run= True)
    if resp.errors:
        raise RuntimeError(resp.errors)

    resp = client.add_rules(rules)
    if resp.errors:
        raise RuntimeError(resp.errors)

    print(client.get_rules())

    try:
        client.filter()
    except KeyboardInterrupt:
        client.disconnect()

    return ('Done')

#use to extract english using rate for streaming data, with mapreduce
"""
@bp.route("/immirate/")
def process_data():
    englishRate.sync(db)
    enrate_s = englishRate(db)

    for row in enrate_s:
        print(row.value)
    return ("rate calcluatd")
"""
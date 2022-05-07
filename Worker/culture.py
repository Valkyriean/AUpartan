from app import dbc
import re
import json
from tweepy import StreamingClient, Tweet, StreamRule
import tweepy
from emot.emo_unicode import UNICODE_EMOJI
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField
from couchdb.design import ViewDefinition
from flaskext.couchdb import Row
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Define function for converting emojis to text for further analysing
def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text.replace("_"," ")

# Setup views and designed documents for storing and querying tweets
manager = CouchDBManager()
class CityLang(Document):
    doc_type = 'CityLang'
    _id = TextField()
    city_name = TextField()
    lang_type = TextField()
    tweet_emo = FloatField()
manager.add_document(CityLang)

# Tweet API Streaming
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHFbAEAAAAA0oBVG5orLLErnyAqw2po3fOae5w%3D4lgZWoMOyGG496F2aNACoKOdDCaDnxqret6oFPLToE244O6Tx6"
CONSUMER_KEY = "K4leUSXBdJwHytayPXdFzEzJN"
CONSUMER_SECRET = "bpyL6MhIsNKRoWDrHj0ou9wHwib7tCm4ob5p3SZam51iDZyqv4"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# design-doc should be the doc-type of historic data document, in string
# Storing design document into database
def view_twitter_lang(design_doc, db):

    totalcount = ViewDefinition(design_doc, 'totallang', '''\
    function(doc){
        emit(doc.doc_type, 1)
    }''','''function(keys, values, rereduce){
              return sum(values);
    }''', wrapper = Row, group = True)

    languagecount = ViewDefinition(design_doc, 'eachlang', '''\
    function(doc){
        emit(doc.lang_type, 1)
    }''','''function(keys, values, rereduce){
              return sum(values);
    }''', wrapper = Row, group = True)

    encount = ViewDefinition(design_doc, 'enlang', '''\
    function(doc){
        if (doc.lang_type == 'en'){
            emit(doc.lang_type, 1)
        };
    }''','''function(keys, values, rereduce){
              return sum(values);
    }''', wrapper = Row, group = True)

    emostat = ViewDefinition(design_doc, 'emocity', '''\
    function(doc){
        emit(doc.lang_type, doc.tweet_emo)
    }''','''function(keys, values, rereduce){
              return sum(values);
    }''', wrapper = Row, group = True)

    totalcount.sync(db)
    languagecount.sync(db)
    encount.sync(db)
    emostat.sync(db)

    return totalcount, languagecount, encount, emostat

totalcount, languagecount, encount, emostat = view_twitter_lang('citylangnew', dbc)

# Path: file path for historical data; public_account:threshold for taking an account as public;db:couchDB databaselanguage:language as target
# Collect twitter information (emotional stat and language type) from the selected city
def citylang(city, follower_limit, bearer_token, api, db):

    class TweetListener(StreamingClient):

        def on_tweet(self, tweet: Tweet):
            text = api.get_status(tweet.id, tweet_mode = "extended")

            if ((text.user.followers_count < follower_limit) and (str(text.id) not in db) and (text.lang != "und")):
                
                # Calculate text emotional stats
                tweet_text = convert_emojis(text.full_text)
                tweet_text = re.sub('http://\S+|https://\S+', '', tweet_text)
                nlp_result = sia.polarity_scores(tweet_text)["compound"]

                # Store the target information into database
                new_lang = CityLang(_id = text.id, city_name = city, lang_type = text.lang, tweet_emo = nlp_result)
                new_lang.store(db)
                
        def on_request_error(self, status_code):
            print(status_code)
            
        def on_connection_error(self):
            self.disconnect
                
    client = TweetListener(bearer_token)
    rules = [StreamRule(value = city)]

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

    #should be added here for 
    try:
        client.filter()
    except KeyboardInterrupt:
        client.disconnect()

    return ('Done')

# Activate the streaming harvest machine based on the selected city name string
citylang("Melbourne", 3000, BEARER_TOKEN, api, dbc) 

# Function to generate pre-cooked data, store it into new summary database and return it as a json file
def view_twitter_stream(viewdef, db):

    language_stat = viewdef(db)

    rate_dict = {}
    for row in language_stat:
        rate_dict[row.key]= row.value
    
    print(rate_dict)
    return json.dumps(rate_dict, indent = 4)

# Call the view_twitter_stream function to compute the summarised data of all city language statistic
view_twitter_stream(totalcount, dbc)
view_twitter_stream(languagecount, dbc)
view_twitter_stream(encount, dbc)
view_twitter_stream(emostat, dbc)
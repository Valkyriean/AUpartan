from tweepy import StreamingClient, Tweet, StreamRule
import tweepy
from tokenize import group
import tweepy
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField
from couchdb.design import ViewDefinition
from flaskext.couchdb import Row


bp = Blueprint("streaming", __name__, url_prefix="/streaming")

if db_enable:
    try:
        db = couch['citylang']
    except:
        db = couch.create('citylang')

manager = CouchDBManager()

class CityLang(Document):
    doc_type = 'CityLang'
    _id = TextField()
    city_name = TextField()
    lang_type = TextField()
    tweet_text = TextField()

manager.add_document(CityLang)

englishRate = ViewDefinition('CityLang', 'enRate', '''\
    function(doc){
        if (doc.lang_type == 'en'){
            emit(doc.city_name, 1);
        }else{
            emit(doc.city_name, 0);
        }
    }''','''function(keys, values, rereduce){
              return sum(values) / values.length;
    }
    ''', wrapper = Row, group = True)

# Tweet API Streaming
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHFbAEAAAAA0oBVG5orLLErnyAqw2po3fOae5w%3D4lgZWoMOyGG496F2aNACoKOdDCaDnxqret6oFPLToE244O6Tx6"
CONSUMER_KEY = "K4leUSXBdJwHytayPXdFzEzJN"
CONSUMER_SECRET = "bpyL6MhIsNKRoWDrHj0ou9wHwib7tCm4ob5p3SZam51iDZyqv4"
bearer_token = BEARER_TOKEN
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

follower_limit = 3000
city = 'Melbourne'


@bp.route("/")
def citylang():
    class TweetListener(StreamingClient):

        def on_tweet(self, tweet: Tweet):
            text = api.get_status(tweet.id, tweet_mode = "extended")

            if ((text.user.followers_count < follower_limit) and (text.id not in db)):
                new_lang = CityLang(_id = text.id, city_name = city, lang_type = tweet.lang, tweet_text = tweet.text)
                new_lang.store(db)
                
        def on_request_error(self, status_code):
            print(status_code)
            
        def on_connection_error(self):
            self.disconnect
                
    client = TweetListener(bearer_token)
    keywords = "Melbourne"
    rules = [
        StreamRule(value = keywords)
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
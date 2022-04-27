import tweepy,os
import re
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField
from couchdb.design import ViewDefinition

bp = Blueprint("geotweet", __name__, url_prefix="/geotweet")

# Setup database in couchdb for stroing tweet information
try:
    db = couch['tweet']
except:
    db = couch.create('tweet')

try:
    db_geo = couch["geodata"]
except:
    db = couch.create("geodata")

manager = CouchDBManager()

# Setup views and designed documents for storing and querying tweets
viewgeo = ViewDefinition("geodata", 'value', '''
    function(doc){
        if (doc.doc_type == 'sa3geo'){
            emit(doc._id, doc.coor_info);
        };
    }''')

class tweet(Document):
    doc_type = 'tweet'
    _id = TextField()
    topic = TextField()
    text = TextField()
    location_id = TextField()
    time = TextField()

#establish the user class, retweet class, like class may be needed
class tweetuser(Document):
    doc_type = 'tweetuser'
    userid = TextField()
    name = TextField()


manager.add_document(tweet)

# Setup api key and api key secret for using tweepy (elevated version is required)
auth = tweepy.OAuthHandler(os.environ.get('API_KEY', None), os.environ.get('API_KEY_SECRET', None))
api = tweepy.API(auth, wait_on_rate_limit=True)

# Collect the target information from twitter with inserted keyword and store it / them into couchdb in a designed structure
@bp.route("/<select_topic>/")
def harvest_tweet(select_topic):

    viewgeo.sync(db_geo)

    for row in viewgeo(db_geo):

        tweets = api.search_tweets(select_topic, geocode = row.value, lang = "en", tweet_mode = "extended") 
        
        for i in tweets:
            if db_enable:
                if str(i.id) not in db:
                    text = i.full_text
                    new_text = re.sub('http://\S+|https://\S+', '', text)
                    new_tweet = tweet(_id = str(i.id), topic = select_topic, text = new_text, location_id = row.key, time = i.created_at)
                    new_tweet.store(db)
                    #add the line to read the user of this tweet
                    new_user = tweetuser(userid=row.user['id_str'], name=row.user['name'])

    return ("done")
import tweepy
import os
import re
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField
from couchdb.design import ViewDefinition

bp = Blueprint("sandtweet", __name__, url_prefix="/sandtweet")

try:
    db_geo = couch["geodata"]
except:
    db = couch.create("geodata")

# Setup database in couchdb for stroing tweet information
try:
    db = couch['sandtweet']
except:
    db = couch.create('sandtweet')

manager = CouchDBManager()

# Setup views and designed documents for storing and querying tweets
viewgeo = ViewDefinition("geodata", 'value', '''
    function(doc){
        if (doc.doc_type == 'sa3geo'){
            emit(doc._id, doc.coor_info);
        };
    }''')

class Sandtweet(Document):
    doc_type = 'sandtweet'
    _id = TextField()
    topic = TextField()
    text = TextField()
    location_id = TextField()
    time = TextField()

manager.add_document(Sandtweet)

# Setup api key and api key secret for using tweepy (elevated & sandbox version is required)
auth = tweepy.OAuthHandler(os.environ.get('API_KEY', None), os.environ.get('API_KEY_SECRET', None))
api = tweepy.API(auth, wait_on_rate_limit=True)

@bp.route("/<select_topic>/")
def harvest_sandtweet(select_topic):

    viewgeo.sync(db_geo)

    for row in viewgeo(db_geo):

        query_string = str(select_topic) + " lang:en point_ratius:" + row.value
        tweets = api.search_full_archive(label = "Relax", query = query_string, fromDate = 202001040000, toDate = 202010040000) 


        tweets = api.search_tweets(select_topic, geocode = row.value, lang = "en", tweet_mode = "extended")

        for i in tweets:
            id = (i.id)
            test = api.get_status(id, tweet_mode="extended")
            print(test.full_text)

        for i in tweets:
            if db_enable:
                if str(i.id) not in db:
                    text = i.full_text
                    new_text = re.sub('http://\S+|https://\S+', '', text)
                    new_tweet = Sandtweet(_id = str(i.id), topic = select_topic, text = new_text, location_id = row.key, time = i.created_at)
                    new_tweet.store(db)

    return ("done")

# 
# tweets = api.search_full_archive(label = "Relax", query = "covid lang:en point_radius:[144.96248 -37.81048 3km]", fromDate = 202001010000, toDate = 202004250000) 

'''for i in tweets:
    id = (i.id)
    test = api.get_status(id, tweet_mode="extended")
    # print(test.full_text)'''
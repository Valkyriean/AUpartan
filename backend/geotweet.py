import  tweepy
import secret
import csv
import pandas as pd
import re
from pickle import TRUE
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, ListField, BooleanField
from couchdb.design import ViewDefinition

bp = Blueprint("geotweet", __name__, url_prefix="/geotweet")

# Setup database in couchdb for stroing tweet information
try:
    db = couch['tweet']
except:
    db = couch.create('tweet')

manager = CouchDBManager()

# Setup views and designed documents for storing and querying tweets
view = ViewDefinition("tweet", 'value', '''
    function(doc){
        if (doc.doc_type == 'tweet'){
            emit(doc.id, doc.text);
        };
    }''')

class tweet(Document):
    doc_type = 'tweet'
    _id = TextField()
    topic = TextField()
    text = TextField()
    location = TextField()
    time = TextField()

manager.add_document(tweet)

# Setup api key and api key secret for using tweepy (elevated version is required)
auth = tweepy.OAuthHandler(secret.key, secret.keysecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Collect the target information from twitter with inserted keyword and store it / them into couchdb in a designed structure
@bp.route("/<select_topic>/")
def store_aurin(select_topic):

    tweets = api.search_tweets(select_topic, geocode= "-37.81011,144.96391,1.5km", lang="en", tweet_mode = "extended") 
    
    for i in tweets:
        if db_enable:
            if str(i.id) not in db:
                text = i.full_text
                new_text = re.sub('http://\S+|https://\S+', '', text)
                new_tweet = tweet(id = str(i.id), topic = select_topic, text = new_text, location = "-37.81011,144.96391,1.5km", time = i.created_at)
                new_tweet.store(db)
    
    return ("done")
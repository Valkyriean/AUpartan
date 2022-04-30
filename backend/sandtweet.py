import tweepy
import os
import re
# from flask import Blueprint
# from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField
from couchdb.design import ViewDefinition
import pandas as pd

#bp = Blueprint("sandtweet", __name__, url_prefix="/sandtweet")

# Setup database in couchdb for stroing tweet information
'''try:
    db = couch['sandtweet']
except:
    db = couch.create('sandtweet')

manager = CouchDBManager()'''

class Sandtweet(Document):
    doc_type = 'sandtweet'
    _id = TextField()
    topic = TextField()
    text = TextField()
    location_id = TextField()
    time = TextField()

API_KEY = "K4leUSXBdJwHytayPXdFzEzJN"
API_KEY_SECRET = "bpyL6MhIsNKRoWDrHj0ou9wHwib7tCm4ob5p3SZam51iDZyqv4"

# manager.add_document(Sandtweet)

# Setup api key and api key secret for using tweepy (elevated & sandbox version is required)
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def harvest_sandtweet(select_topic):
    geo_data = pd.read_csv("../Data/Geo/sa3_geoinfo.csv")
    test = geo_data["SA3_GEOINFO"][0]
    #print(test)
    
    
    query_string = str(select_topic) + " lang:en point_radius:" + test
    print(query_string)
    
    tweets = api.search_full_archive(label = "Relax", query = query_string, fromDate = 202001040000, toDate = 202010040000) 

    for i in tweets:
        id = (i.id)
        test = api.get_status(id, tweet_mode="extended")
        print(test.user.id)#this will return id as int, if want string, using".id_str"
        break
    '''
    for i in tweets:
        if db_enable:
            if str(i.id) not in db:
                text = i.full_text
                new_text = re.sub('http://\S+|https://\S+', '', text)
                new_tweet = Sandtweet(_id = str(i.id), topic = select_topic, text = new_text, location_id = row.key, time = i.created_at)
                new_tweet.store(db)
    '''

    return ("done")

harvest_sandtweet("Covid")


# 
# tweets = api.search_full_archive(label = "Relax", query = "covid lang:en point_radius:[144.96248 -37.81048 3km]", fromDate = 202001010000, toDate = 202004250000) 

'''for i in tweets:
    id = (i.id)
    test = api.get_status(id, tweet_mode="extended")
    # print(test.full_text)'''
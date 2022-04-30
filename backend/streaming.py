import tweepy
import os
from tweepy import StreamingClient, Tweet, StreamRule
import re
from tokenize import group
import tweepy
from flask import Blueprint
from app import db_enable, couch
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, IntegerField, ListField, FloatField
from couchdb.design import ViewDefinition
from flaskext.couchdb import Row
import functools, threading

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIHFbAEAAAAA0oBVG5orLLErnyAqw2po3fOae5w%3D4lgZWoMOyGG496F2aNACoKOdDCaDnxqret6oFPLToE244O6Tx6"

bearer_token = BEARER_TOKEN

class TweetListener(StreamingClient):

    def on_tweet(self, tweet: Tweet):
        print(tweet.__repr__)
        
    def on_request_error(self, status_code):
        print(status_code)
    
    def on_connection_error(self):
        self.disconnect
        
client = TweetListener(bearer_token)

rules = [
    StreamRule(value="Melbourne lang:en")
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

# Store the city voice information
if db_enable:
    try:
        db = couch['cityvoice']
    except:
        db = couch.create('cityvoice')

manager = CouchDBManager()

class CityVoice(Document):
    doc_type = 'CityVoice'
    _id = TextField()
    city_id = TextField()
    tweet_topic = TextField()
    tweet_content = TextField()

manager.add_document(CityVoice)
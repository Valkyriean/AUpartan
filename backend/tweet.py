#from flask import Blueprint
import tweepy, os
#import app
from flaskext.couchdb import Document, CouchDBManager
from couchdb.mapping import TextField, FloatField

#bp = Blueprint("tweet", __name__, url_prefix="/t")
BEARER_TOKEN = os.environ.get('BEARER_TOKEN', None)

client = tweepy.Client(BEARER_TOKEN)

#@bp.route("/c")
def check():
    return os.environ.get('BEARER_TOKEN', None)


class SearchTweet(Document):
    _id = TextField
    #.....requirement attribute



#@bp.route("/s/<keyword>")
def search(keyword, db):
    result = client.search_recent_tweets(keyword, max_results=10)
    print(result.data)
    #ret = ""
    for d in result.data:
        #anti-dublication and write in process should be here





        #db.save({'id':d.id, 'text':d.text, 'maintag': keyword})
        #ret += "<h1>" + d.text + "</h1>"
    return ret


"""
#@bp.route("/stream")
def stream():
    stream_client = tweepy.StreamingClient(BEARER_TOKEN)
    stream_client.add_rules("covid")
    res = stream_client.filter()
    print(res)
    return "check standard output"
""" 
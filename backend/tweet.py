from flask import Blueprint
import tweepy, os
from app import db, db_enable

bp = Blueprint("tweet", __name__, url_prefix="/t")
BEARER_TOKEN = os.environ.get('BEARER_TOKEN', None)

client = tweepy.Client(BEARER_TOKEN)

@bp.route("/c")
def check():
    return os.environ.get('BEARER_TOKEN', None)


@bp.route("/s/<keyword>")
def search(keyword):
    result = client.search_recent_tweets(keyword, max_results=10)
    print(result.data)
    ret = ""
    for d in result.data:
        if db_enable:
            db.save({'id':d.id, 'text':d.text, 'maintag': keyword})
        ret += "<h1>" + d.text + "</h1>"
    return ret

@bp.route("/stream")
def stream():
    stream_client = tweepy.StreamingClient(BEARER_TOKEN)
    stream_client.add_rules("covid")
    res = stream_client.filter()
    print(res)
    return "check standard output"
    
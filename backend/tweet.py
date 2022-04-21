from flask import Blueprint
import tweepy, os
from app import db

bp = Blueprint("tweet", __name__, url_prefix="/t")

client = tweepy.Client(os.environ.get('BEARER_TOKEN', None))

@bp.route("/c")
def check():
    return os.environ.get('BEARER_TOKEN', None)


@bp.route("/s/<keyword>")
def tweet(keyword):
    result = client.search_recent_tweets(keyword, max_results=10)
    print(result.data)
    ret = ""
    for d in result.data:
        db.save({'id':d.id, 'text':d.text})
        ret += "<h1>" + d.text + "</h1>"
    return ret
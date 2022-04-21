from flask import Blueprint
import tweepy, os

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
        ret += "<h1>" + d.text + "</h1>"
    return ret
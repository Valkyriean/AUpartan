import os
from flask import Flask
from couchdb import Server
from flask_cors import CORS

SECRET_KEY = os.environ.get('SECRET_KEY', None)
DB_USERNAME = os.environ.get('DB_USERNAME', None)
DB_PASSWORD = os.environ.get('DB_PASSWORD', None)
# app setup
app = Flask(__name__)
CORS(app)
app.secret_key = SECRET_KEY
# db setup
db_enable = True
db = None
try:
    couch = Server()
    couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)
    try:
        db = couch['ccc']
    except:
        db = couch.create('ccc')
except:
    print("WARRING: database is not running\n")
    db_enable = False

# route
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# import tweet
# app.register_blueprint(tweet.bp)

import aurin
app.register_blueprint(aurin.bp)

# import geotweet
# app.register_blueprint(geotweet.bp)

# import geosa3
# app.register_blueprint(geosa3.bp)

import historic
app.register_blueprint(historic.bp)

import hissummary
app.register_blueprint(hissummary.bp)

import streaming
app.register_blueprint(streaming.bp)
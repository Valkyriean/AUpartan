import os
from flask import Flask
from couchdb import Server

SECRET_KEY = os.environ.get('SECRET_KEY', None)
DB_USERNAME = os.environ.get('DB_USERNAME', None)
DB_PASSWORD = os.environ.get('DB_PASSWORD', None)
# app setup
app = Flask(__name__)
app.secret_key = SECRET_KEY
# db setup
db_enable = True
db = None
try:
    couch = Server()
    couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)
    db = couch['ccc']
except:
    print("WARRING: database is not running\n")
    db_enable = False
# route
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

import tweet
app.register_blueprint(tweet.bp)
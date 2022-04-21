from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', None)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



import tweet
app.register_blueprint(tweet.bp)
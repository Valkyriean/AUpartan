import os
import sys
import subprocess
import secret
import importlib.util

'''
Running instruction:
Fill and put following in <secret.py> in your root

SECRET_KEY = "nana7mi"
BEARER_TOKEN = "<FILL ME>"
DB_USERNAME="admin"
DB_PASSWORD="<FILL ME>"

'''

dev = True

flask = importlib.util.find_spec("flask")
gunicorn = importlib.util.find_spec("gunicorn")
tweepy = importlib.util.find_spec("tweepy")

if flask is None or gunicorn is None or tweepy is None:
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

os.environ['SECRET_KEY'] = secret.SECRET_KEY
os.environ['BEARER_TOKEN'] = secret.BEARER_TOKEN
os.environ['DB_USERNAME'] = secret.DB_USERNAME
os.environ['DB_PASSWORD'] = secret.DB_PASSWORD
if dev:
    os.environ['FLASK_ENV'] = "development"
    os.system('cd backend && flask run')
else:
    os.system('cd backend && gunicorn app:app')

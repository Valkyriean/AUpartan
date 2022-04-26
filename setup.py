import os
import sys
import subprocess
import mysecrets
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

os.environ['SECRET_KEY'] = mysecrets.SECRET_KEY
os.environ['BEARER_TOKEN'] = mysecrets.BEARER_TOKEN
os.environ['DB_USERNAME'] = mysecrets.DB_USERNAME
os.environ['DB_PASSWORD'] = mysecrets.DB_PASSWORD
os.environ['KEY']=mysecrets.KEY
os.environ['KEYSECRET']=mysecrets.KEYSECRET

if dev:
    os.environ['FLASK_ENV'] = "development"
    os.system('cd backend && python -m flask run --host=0.0.0.0')
else:
    os.system('cd backend && python -m gunicorn app:app')

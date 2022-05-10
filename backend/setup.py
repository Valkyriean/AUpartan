import os
import sys
import subprocess
import secret
import importlib.util
import platform

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
os.environ['API_KEY']=secret.API_KEY
os.environ['API_KEY_SECRET']=secret.API_KEY_SECRET

if dev:
    os.environ['FLASK_ENV'] = "development"
    if platform.system() == "Windows":
        os.system('flask run --host=0.0.0.0 --port=5001')
    else:
        os.system('python3 -m flask run --host=0.0.0.0 --port=5001')
else:
    if platform.system() == "Windows":
        os.system('gunicorn app:app')
    else:
        os.system('python3 -m gunicorn --bind 0.0.0.0:3000 --workers=2 app:app')
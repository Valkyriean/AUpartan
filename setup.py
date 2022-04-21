import os
import sys
import subprocess
import secret
import importlib.util

'''
Running instruction:
Make sure to create secret.py at root and set SECRET_KEY, and BEARER_TOKEN


'''


dev = True

spec = importlib.util.find_spec("flask")
if spec is None:
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

os.environ['SECRET_KEY'] = secret.SECRET_KEY
os.environ['BEARER_TOKEN'] = secret.BEARER_TOKEN
os.environ['FLASK_ENV'] = "development"
if dev:
    os.system('cd backend && flask run')
else:
    os.system('cd backend && gunicorn app:app')

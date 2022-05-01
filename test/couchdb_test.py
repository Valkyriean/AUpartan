import subprocess
from couchdb import Server

subprocess.check_call(["pip", "install", "CouchDB"])

import couchdb
DB_USERNAME="admin"
DB_PASSWORD="meiyoumima"
couch = Server()
couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)
try:
    db = couch['test']
except:
    db = couch.create('test')
db.save({'contant':'test'})
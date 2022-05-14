import subprocess
from couchdb import Server

subprocess.check_call(["pip", "install", "CouchDB"])

import couchdb
DB_USERNAME="admin"
DB_PASSWORD="admin"
couch = Server()
couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)
# try:
#     db = couch['test']
# except:
#     db = couch.create('test')
# db.save({'contant':'test'})


def get_city_db():
    res = []
    for d in couch:
        d_list = d.split('_')
        if len(d_list) >=3 and d_list[-1] == 'summary' and d_list[1] == "city":
            res.append(d)
    return res

print(get_city_db())
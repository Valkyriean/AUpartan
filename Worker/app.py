import time
import requests
import json 
from couchdb import Server


# Initialise
REQUEST_GAP = 10
GATEWAY_IP = "0.0.0.0"
GATEWAY_PORT = 3000
ID=1
DB_USERNAME= "admin"
DB_PASSWORD= "1999317"

couch = Server()
couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)
try:
    db = couch['historic']
except:
    db = couch.create('historic')

print("Initialized")
# Main loop





"""
while True:
    # Request task from main node
    print("request task from gateway...")
    try: 
        r = requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/task"), json={"id": ID})
        # Do job
        res = r.json()
        print(res)
        if res["status"] == "success":
            
            print("get task id"+ str(res['task']['id']))
            time.sleep(res["task"]["time"])
        else:
            print(res["status"])
            time.sleep(REQUEST_GAP)
    except:
        print("no connection to gateway, retry in 1 sec")
        time.sleep(1)
"""
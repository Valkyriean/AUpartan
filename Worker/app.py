import time
import requests
import json 

# Initialise

# Main loop



REQUEST_GAP = 10
GATEWAY_IP = "localhost"
GATEWAY_PORT = 3000
ID=1

while True:
    # Request task from main node
    print("request task from gateway")
    r = requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/task"), json={"id":1})
    # Do job
    res = r.json()
    print(res)
    if res["status"] == "success":
        
        print("get task id"+ str(res['task']['id']))
        time.sleep(res["task"]["time"])
    else:
        print(res["status"])
        time.sleep(REQUEST_GAP)
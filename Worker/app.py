import time
import requests
import json 
from couchdb import Server
from aurindb import preserve_aurin
from historicdb import preserve_historic
from aurin import aurin_work
from historic import historic_work
from search import search_work
import os 
import sys

# Initialise
REQUEST_GAP = 10
GATEWAY_IP = sys.argv[1]
print(GATEWAY_IP)
GATEWAY_PORT = 3000
WORKER_ID = sys.argv[2]
print(WORKER_ID)
DB_USERNAME= "admin"
DB_PASSWORD= "admin"

couch = Server()
couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)

print("Initialized")
# Main loop

def assign_work(task):
    task_type = task.get("type", None)
    if task_type == "aurin":
        search_level = task.get("level", None)
        search_keyword = task.get("keyword", None)
        aurin_work(couch, search_level, search_keyword)
        return True
    elif task_type == "search":
        keyword = task["keyword"]
        search_work(couch, keyword)
        return True
    elif task_type == "historic":
        keyword = task["keyword"]
        historic_work(couch, keyword)
        return True
    else:
        preserve_name = task.get("task", None)
        if preserve_name == "aurin":
            preserve_aurin(couch)
            return True
        elif preserve_name == "historic":
            preserve_historic(couch)
            return True
        return False



def main():
    while True:
        # Request task from main node
        print("request task from gateway...")
        try: 
            r = requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/get_task"), json={"worker_id": WORKER_ID})
            res = r.json()
            print(res)
            if res.get("status", None) == "success":
                print("get task name"+ str(res['task']['name']))
                task = res.get("task",None)
                task_name = task.get("name", "unnamed")
                print(task)
                if task:
                    print("assigned")
                    succ = assign_work(task)
                    if succ:
                        requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/finish_task"), json={"task_name": task_name})
                    else:
                        requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/failed_task"), json={"task_name": task_name})
                else:
                    print("NO task found")
                    # task not exist
                    # r = requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/failed_task"), json={"task_name": task_name})
            else:
                print(res["status"])
                time.sleep(REQUEST_GAP)
        except:
            print("no connection to gateway")
            time.sleep(REQUEST_GAP)
            
main()
import time
import requests
import json 
from couchdb import Server
from aurin import aurin_work
from historic import historic_work
from search import search_work

# Initialise
REQUEST_GAP = 10
GATEWAY_IP = "0.0.0.0"
GATEWAY_PORT = 3000
WORKER_ID=1
DB_USERNAME= "admin"
DB_PASSWORD= "Relax1017"

couch = Server()
couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)

print("Initialized")
# Main loop

def test():
    ret = search_work(couch, "Election")
    print(ret)

def assign_work(task):
    task_type = task.get("type", None)
    if task_type == "aurin":
        print("Aurin task")
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
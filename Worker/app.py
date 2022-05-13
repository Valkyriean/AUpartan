import time
import requests
from couchdb import Server
from aurindb import preserve_aurin
from historicdb import preserve_historic
from aurin import aurin_work
from historic import historic_work
from search import search_work
import sys
from random import uniform

# Initialise
REQUEST_GAP = 10
GATEWAY_IP = "localhost"
GATEWAY_PORT = 3000
WORKER_IP = "localhost"
DB_USERNAME= "admin"
DB_PASSWORD= "admin"
if len(sys.argv) == 3:
    GATEWAY_IP = sys.argv[1]
    WORKER_IP = sys.argv[2]
print(GATEWAY_IP)
print(WORKER_IP)

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
    elif task_type == "preserve":
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
            r = requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/get_task"), json={"worker_ip": WORKER_IP})
            res = r.json()
            print(res)
            if res.get("status", None) == "success":
                print("get task name"+ str(res['task']['name']))
                task = res.get("task",None)
                task_name = task.get("name", "unnamed")
                print(task)
                if task:
                    print("task valid")
                    flag = assign_work(task)
                    # flag = True
                    # time.sleep(5)
                    if flag:
                        print("Finished")
                        requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/finish_task"), json={"task_name": task_name})
                    else:
                        print("Failed")
                        requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/failed_task"), json={"task_name": task_name})
                else:
                    print("NO task found")
                    # task not exist
                    # r = requests.post(("http://"+GATEWAY_IP+":"+str(GATEWAY_PORT)+"/failed_task"), json={"task_name": task_name})
            else:
                print(res["status"])
                time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
        except:
            print("no connection to gateway")
            time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
            
main()
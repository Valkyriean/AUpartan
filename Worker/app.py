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
from datetime import timedelta, datetime


# Initialise
REQUEST_GAP = 15
WORKER_IP = "localhost"
DB_USERNAME= "admin"
DB_PASSWORD= "admin"
if len(sys.argv) == 2:
    WORKER_IP = sys.argv[1]
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


try:
    pending = couch['pending']
except:
    pending = couch.create('pending')

try:
    working = couch['working']
except:
    working = couch.create('working')
    
try:
    finished = couch['finished']
except:
    finished = couch.create('finished')
timeout = timedelta(days=1)

def try_work(task):
    task['timeout'] = str(datetime.now()+timeout)
    task.pop('_rev')
    working.save(task)
    print("Work on " + task['name'])
    result = assign_work(task)
    # result = True
    if result:
        working.delete(task)
        task.pop('_rev')
        finished.save(task)
    else:
        task.pop('_rev')
        pending.save(task)

# use three db
def main():
    while True:
        try:
            # Try redo timeouted task
            print("run")
            if len(working) is not 0: 
                print("have running")    
                for t in working:
                    task = working[t]
                    if task['timeout'] < str(datetime.now()):
                        print("found timeout task "+ t)
                        working.delete(task)
                        try_work(task)
                        time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
                        break
            # take task from pending
            if len(pending) is 0:
                print("no task left, go sleep")
                time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
                continue
            else:
                for t in pending:
                    task = pending[t] 
                    pre = task.get('prerequisite', None)
                    if pre == None or pre in finished:
                        print("found pending can run "+t)
                        pending.delete(task)
                        try_work(task)                    
                    else:
                        print("pre not ready "+t)
                        time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
            # time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
        except Exception as e: 
            print(repr(e))
            time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
            continue
        time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
    
            
            
            
tasks = [{"name": "aurin_preserve", 
                "type" : "preserve",
                "task" : "aurin"},
{"name": "historic_preserve", 
                "type" : "preserve",
                "task" : "historic"},
{"name": "aurin_payroll",
                "type": "aurin",
                "keyword": "payroll",
                "level" : "sa3",
                "prerequisite":"aurin_preserve"},
{"name": "aurin_income",
                "type": "aurin",
                "keyword": "income",
                "level" : "sa3",
                "prerequisite":"aurin_preserve"},
{"name": "aurin_immigration",
                "type": "aurin",
                "keyword": "immigration",
                "level" : "city",
                "prerequisite":"aurin_preserve"},
{"name": "aurin_salary",
                "type": "aurin",
                "keyword": "salary",
                "level" : "city",
                "prerequisite":"aurin_preserve"},
{"name": "search_election",
                "type": "search",
                "keyword": "Election"},
{"name": "search_crime",
                "type": "search",
                "keyword": "crime"},
{"name": "historic_crime",
                "type": "historic",
                "keyword": "crime",
                "prerequisite":"historic_preserve"},
{"name": "historic_all",
                "type": "historic",
                "keyword": "all",
                "prerequisite":"historic_preserve"}]
# for t in tasks:
#     # if t['name'] not in pending:
#         t['_id'] = t['name']
#         t['state'] = 'pending'
#         pending.save(t)

# def work(task):
#     task['timeout'] = str(datetime.now()+timeout)
#     task['state'] = "working"
#     print(task)
#     # time.sleep(1)
#     pending.save(task)
#     print("try work on "+ task['name'])
#     # result = assign_work(task)
#     result = True
#     time.sleep(5)
#     if result:
#         task['state'] = "finished"
#         pending.save(task)
#     else:
#         task['state'] = "pending"
#         pending.save(task)

# use one db only 

# def main():
#     while True:
#         if len(pending) == 0:
#             print("no task left, go sleep")
#             time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
#             continue
#         for t in pending:
#             task = pending[t]
#             if task['state'] == 'working' and task['timeout'] < str(datetime.now()):
#                 print("found expired "+t)
#                 work(task)
#             if task['state'] == 'pending':
#                 print("found pending "+t)
#                 pre = pending[t].get('prerequisite', None)
#                 if pre == None or pre not in pending or (pre in pending and pending[pre]['state'] == 'finished'):
#                     print("found pending pre mate"+t)
#                     work(task)                    
#                 else:
#                     print("pre not ready "+t)
                
#                 # continue
#             time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))

# try:
#     main()
# except Exception as e: 
#     print(repr(e))
    
main()
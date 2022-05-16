# Qianjun Ding 1080391
# Zhiyuan Gao 1068184
# Jiachen Li 1068299
# Yanting Mu 1068314
# Chi Zhang 1067750

import time
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
DB_USERNAME = "admin"
DB_PASSWORD = "admin"
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
        #aurin_work(couch, search_level, search_keyword)
        return aurin_work(couch, search_level, search_keyword)
    elif task_type == "search":
        keyword = task["keyword"]
        #search_work(couch, keyword)
        return search_work(couch, keyword)
    elif task_type == "historic":
        keyword = task["keyword"]
        #historic_work(couch, keyword)
        return historic_work(couch, keyword)
    elif task_type == "preserve":
        preserve_name = task.get("task", None)
        if preserve_name == "aurin":
            # preserve_aurin(couch)
            return preserve_aurin(couch)
        elif preserve_name == "historic":
            # preserve_historic(couch)
            return preserve_historic(couch)
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
                        print("found timeout task " + t)
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
                        break
                    else:
                        print("pre not ready "+t)
                        time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
            # time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
        except Exception as e:
            print(repr(e))
            time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))
            continue
        time.sleep(uniform(REQUEST_GAP-0.5, REQUEST_GAP+0.5))


main()

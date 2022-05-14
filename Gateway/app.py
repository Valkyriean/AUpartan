import queue
from flask import Flask, jsonify, request, make_response, send_file
from flask_cors import CORS
from datetime import timedelta, datetime
from readSummary import extract_summary

from couchdb import Server


# Initialise

DB_USERNAME= "admin"
DB_PASSWORD= "admin"
couch = Server()
couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)


# Gateway backend following ReSTful
app = Flask(__name__, static_url_path="")
CORS(app)

queueing_task = queue.Queue()
# (due date, task, worker IP)
working_task = []
finished_task = []
timeout = timedelta(days=1)

# scenario dictionary
scenarioDict = dict()

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
                "keyword": "Election"
},

 {"name": "search_crime",
                "type": "search",
                "keyword": "crime"
},

{"name": "historic_crime",
                "type": "historic",
                "keyword": "crime",
                "prerequisite":"historic_preserve"
},

{"name": "historic_all",
                "type": "historic",
                "keyword": "all",
                "prerequisite":"historic_preserve"
}]

# queueing_task.put(preserve_task_1)
# queueing_task.put(preserve_task_2)
# queueing_task.put(example_task_1)
# queueing_task.put(example_task_2)
# queueing_task.put(example_task_3)
# queueing_task.put(example_task_4)
# queueing_task.put(example_task_5)
# queueing_task.put(example_task_6)
# queueing_task.put(example_task_7)
# queueing_task.put(example_task_8)


scenarioDict["Income (sa3) VS overall sentiment"] = [{"name": "aurin_income", "level": "sa3"}, {"name": "historic_all", "method": "sentiment"}]
scenarioDict["Income (city) VS attitude toward election"] = [{"name": "aurin_salary", "level": "city"}, {"name": "search_election", "method": "sentiment"}]
scenarioDict["Income (city) VS count of mentioning crime"] = [{"name": "aurin_salary", "level": "city"}, {"name": "search_crime", "method": "count"}]
scenarioDict["Crime count (sa3)"] = [{"name": "historic_crime", "method": "count"}]

# ##### For Testing Only #####
# finished_task.append(example_task_1)
# finished_task.append(example_task_2)
# finished_task.append(example_task_3)
# finished_task.append(example_task_4)
# finished_task.append(example_task_5)
# finished_task.append(example_task_6)
# ##### Remove After Front End Testing #####

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





@app.route('/initdb')
def init_db():
    try:
        pending = couch.create('pending')
    except:
        # pending = couch['pending']
        couch.delete("pending")
        pending = couch.create('pending')

    try:    
        working = couch.create('working')
        # working = couch['working']
    except:
        couch.delete("working")
        working = couch.create('working')
        
    try:
        finished = couch.create('finished')
        # finished = couch['finished']
    except:
        couch.delete("finished")
        finished = couch.create('finished')

    for t in tasks:
        if t['name'] not in pending:
            t['_id'] = t['name']
            t['state'] = 'pending'
            pending.save(t)
    return {"status":"success"}, 200

@app.route('/init_finished')
def init_db_finished():
    try:
        pending = couch.create('pending')
    except:
        # pending = couch['pending']
        couch.delete("pending")
        pending = couch.create('pending')

    try:    
        working = couch.create('working')
        # working = couch['working']
    except:
        couch.delete("working")
        working = couch.create('working')
        
    try:
        finished = couch.create('finished')
        # finished = couch['finished']
    except:
        couch.delete("finished")
        finished = couch.create('finished')

    for t in tasks:
        if t['name'] not in finished:
            t['_id'] = t['name']
            t['state'] = 'pending'
            finished.save(t)
    return {"status":"success"}, 200




def get_pending():
    return list(pending)
def get_working():
    return list(working)
def get_finished():
    return list(finished)

# print(list(pending))
# print(len(working))
# for i in pending:
#     print(pending[i]["type"])

# for i in pending:
#    pending[i]["type"] = "new"
#    pending.save(pending[i])
# for i in pending:
#     print(pending[i]["type"])
# working pool
app.task_start_time = datetime.now() - timedelta(seconds=1)


# @app.route('/get_task', methods=['POST'])
# async def get_task():
#     worker_ip = str(request.json.get("worker_ip"))
#     for t in working:
#         if working[t]['timeout'] < str(datetime.now()):
#             working[t]['timeout'] = str(datetime.now()+timeout)
#             working.save(working[t])
#             return {"status":"success", "task":task}
#     # take task from task queue
#     if len(working) == 0:
#         print("no work")
#         return {"status":"no_work"}
#     task = queueing_task.get()
#     prerequisite = task.get("prerequisite", None)
#     limit = queueing_task.qsize()
#     index = 0
#     while prerequisite not in finished_task and prerequisite != None:
#         if index > limit:
#             print("No fulfilled task")
#             return {"status":"no prerequisite fulfilled task"}
#         print(f"prerequisite {prerequisite} not fulfilled for task "+str(task.get("name")))
#         queueing_task.put(task)
#         task = queueing_task.get()
#         prerequisite = task.get("prerequisite", None)
#         index += 1
#     print("Task " + str(task["name"]) + " got by worker " + worker_ip)
#     working_task.append((datetime.now()+timeout,task, worker_ip))
#     return {"status":"success", "task":task}


# @app.route('/finish_task', methods=['POST'])
# def finish_task():    
#     print(str(queueing_task.qsize())+"\n")
#     print(str(working_task)+"\n")
#     print(str(finished_task)+"\n")
#     json_data = request.json
#     task_name = json_data.get('task_name', "nameless task")
#     if task_name in finished_task:
#         return {"status":"success"}, 200
#     print("Finish " + str(task_name))
#     flag = False
#     for t in working_task:
#         if t[1].get("name", None) == task_name:
#             working_task.remove(t)
#             flag = True
#             break
#     if flag:
#         finished_task.append(task_name)
#     return {"status":"success"}, 200

        
# @app.route('/failed_task', methods=['POST'])
# async def failed_task():
#     json_data = request.json
#     task_name = json_data.get('task_name', "nameless task")
#     if task_name in finished_task:
#         return {"status":"success"}, 200
#     print("Failed " + str(task_name))
#     for t in working_task:
#         if t[1].get("name", None) == task_name:
#             temp = t
#             working_task.remove(t)
#             working_task.insert(0, (datetime.now(), temp[1], temp[2]))
#             break
#     return {"status":"success"}, 200
        
# Front end
@app.route('/working_task', methods=['GET'])
def get_working_task():
    return str(get_working)

@app.route('/finished_task', methods=['GET'])
def get_finished_task():
    return str(get_finished())


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


##### Front end serving #####
# Serve the static file to client's browser

# get all task names with "city" or "sa3" on its second section
print(scenarioDict.keys())

def getCoord(city):
    cityDict = {
        "Melbourne": [-37.840935,144.946457],
        "Sydney": [-33.865143, 151.209900],
        "Canberra": [-35.282001, 149.128998],
        "Brisbane": [-27.470125, 153.021072],
        "Perth": [-31.953512, 115.857048],
        "Adelaide": [-34.846111, 138.503052],
        "Hobart": [-42.880554, 147.324997]
    }
    return cityDict[city]

def getAurinTasksName(scale):
    tasks = []
    for name in couch:
        try:
            if (str(name).split('_'))[1] == scale: tasks.append(name)
        except:
            pass
    return tasks

def translateDBAurin2stdTask(nameDB):
    items = nameDB.split("_")
    ret = {"name": "aurin_" + items[2],
           "type": "aurin",
           "keyword": items[2],
           "level" : items[1],
           "prerequisite":"aurin_preserve"
          }
    return ret

# trst if a given task exist in a queue or list
def check_finished(task_name):
    if task_name in get_finished():
        return True
    return False

def check_global(task_name):
    if check_finished(task_name):
        return True
    elif task_name in get_working():
        return True
    elif task_name in get_finished():
        return True
    return False

@app.route("/add_task")
def add_task():
    task = request.json
    addTask(task)
    return {"status":"success"}, 200


@app.route("/add_task_working")
def add_task():
    task = request.json
    task['_id'] = task["name"]
    working.save(task)
    return {"status":"success"}, 200

@app.route("/add_task_finished")
def add_task():
    task = request.json
    task['_id'] = task["name"]
    finished.save(task)
    return {"status":"success"}, 200

# append task to queueing_task if there's no duplication
# return true when task successfully added
def addTask(task):
    if not check_global(task["name"]): 
        task['_id'] = task["name"]
        pending.save(task)
        return True
    return False

# get all scenario ready for ploting
# "ready" means all tasks involved are completed
def getScenarioAvailable():
    print("finished tasks: " + str(get_finished()))
    availableScenarios = []
    for scenario in scenarioDict.keys():
        print("testing scenario: " + scenario )
        flag = True
        for task in scenarioDict[scenario]:
            print(task["name"])
            if not check_finished(task["name"]):
                flag = False
        if flag: availableScenarios.append(scenario)
    return availableScenarios

# basic routings
@app.route('/', methods=["GET"])
def get_index():
    return send_file('./instance/index.html')

@app.route('/static/js/<filename>', methods=["GET"])
def get_js(filename):
    return send_file('./instance/static/js/{0}'.format(filename))

@app.route('/static/css/<filename>', methods=["GET"])
def get_css(filename):
    return send_file('./instance/static/css/{0}'.format(filename))

# @app.route('/img/<filename>', methods=["GET"])
# def get_img(filename):
#     return send_file('./static/dist/img/{0}'.format(filename))

# @app.route('/media/<filename>', methods=["GET"])
# def get_media(filename):
#     return send_file('./static/dist/media/{0}'.format(filename))

@app.route('/favicon.ico', methods=["GET"])
def get_ico():
    return send_file('./instance/favicon.ico')

@app.route('/app/<foo>', methods=["GET"])
def serve(foo):
    return send_file('./instance/index.html')

# handel requests from page "submit"
@app.route('/request/submit', methods = ['GET', 'POST'])
def submit_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "preCalculatedList_SA3":
            print(getAurinTasksName("sa3"))
            return jsonify({"preCalculatedList" : getAurinTasksName("sa3")})
        if json_data["request"] == "preCalculatedList_City":
            print(getAurinTasksName("city"))
            return jsonify({"preCalculatedList" : getAurinTasksName("city")})
        if json_data["request"] == "task":
            scenarioName = json_data["name"]
            if '0-0-word' in json_data.keys():
                if json_data['scale'] == 'City': 
                    taskType = 'search'
                else:
                    taskType = 'historic'
                task_0 = {
                    'name': taskType + '_' + json_data['0-0-word'],
                    'type': taskType,
                    'keyword': json_data['0-0-word'],
                    'level': json_data['scale'],
                    'method': json_data['0-0-process']
                }
            elif '0-0-preCal' in json_data.keys():
                taskType = 'preCalculated'
                task_0 = translateDBAurin2stdTask(json_data['0-0-preCal'])
            else:
                raise IndexError('no valid input')
            
            if '0-1-word' in json_data.keys() or '0-1-preCal' in json_data.keys():
                if '0-1-word' in json_data.keys():
                    if json_data['scale'] == 'City': 
                        taskType = 'search'
                    else:
                        taskType = 'historic'
                    task_1 = {
                        'name': taskType + '_' + json_data['0-1-word'],
                        'type': taskType,
                        'keyword': json_data['0-1-word'],
                        'level': json_data['scale'],
                        'method': json_data['0-1-process']
                    }
                elif '0-1-preCal' in json_data.keys():
                    taskType = 'preCalculated'
                    task_1 = translateDBAurin2stdTask(json_data['0-1-preCal'])
                print({scenarioName: [task_0, task_1]})
                ##### add scenario {scenarioName: [task_0['name'], task_1]} #####
                scenarioDict[scenarioName] = [task_0, task_1]
                ##### add task set(task_0, task_1) #####
                addTask(task_0)
                addTask(task_1)
            else:
                print({scenarioName: [task_0]})
                ##### add scenario {scenarioName: [task_0]} #####
                scenarioDict[scenarioName] = [task_0]
                ##### add task set(task_0) #####
                addTask(task_0)
                pass 
            return jsonify({"state" : "success"})
    except:
        print("something wrong")
        return jsonify({"state" : "failed"})

# handel requests from page "submit"
@app.route('/request/plot', methods = ['GET', 'POST'])
def plot_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "plotList":
            print(getScenarioAvailable())
            return jsonify({"plotList" : getScenarioAvailable()})
        if json_data["request"] == "getData":
            scenarioRequested = json_data["scenario"]
            if len(scenarioDict[scenarioRequested]) == 1:
                raw = extract_summary(couch, scenarioDict[scenarioRequested][0])
                keys = []
                y = []
                for key in raw.keys():
                    keys.append(key)
                    y.append(raw[key])
                print({"data": {"type": "bar", "x": keys, "y": y}, 
                                "titleLabel": scenarioRequested, 
                                "xLabel": "", 
                                "yLabel": scenarioDict[scenarioRequested][0]["name"]
                              })
                return jsonify({"data": {"type": "bar", "x": keys, "y": y}, 
                                "titleLabel": scenarioRequested, 
                                "xLabel": "", 
                                "yLabel": scenarioDict[scenarioRequested][0]["name"]
                              })
            else:
                data_0 = extract_summary(couch, scenarioDict[scenarioRequested][0])
                data_1 = extract_summary(couch, scenarioDict[scenarioRequested][1])
                x = []
                y = []
                keys = []
                for key in data_0.keys():
                    if key in data_1.keys():
                        x.append(data_0[key])
                        y.append(data_1[key])
                        keys.append(key)
                print({"data": {"type": "scatter", "mode": "markers", "x": x, "y": y, "text": keys, "marker": {"size": 15}}, 
                                "titleLabel": scenarioRequested, 
                                "xLabel": scenarioDict[scenarioRequested][0]["name"],
                                "yLabel": scenarioDict[scenarioRequested][1]["name"]
                              })
                return jsonify({"data": {"type": "scatter", "mode": "markers", "x": x, "y": y, "text": keys, "marker": {"size": 15}}, 
                                "titleLabel": scenarioRequested, 
                                "xLabel": scenarioDict[scenarioRequested][0]["name"],
                                "yLabel": scenarioDict[scenarioRequested][1]["name"]
                              })

    except:
        print("something wrong")
        return jsonify({"state" : "failed"})

########################### replace and delete this thing
def get_city_db():
    res = []
    for d in couch:
        d_list = d.split('_')
        if len(d_list) >=3 and d_list[-1] == 'summary' and d_list[1] == "city":
            res.append(d)
    return res

###########################

@app.route('/request/map', methods = ['GET', 'POST'])
def map_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "dataList":
            return jsonify(get_city_db())
        if json_data["request"] == "cityData":
            print("request data: " + json_data["scenario"])
            datadict = extract_summary(couch, json_data["scenario"])
            retDict = dict()
            for name in datadict.keys():
                print(name)
                retDict[name] = [getCoord(name), datadict[name]]
            citys = list(datadict.keys())
            print({"cityList" : citys, "cityData": retDict})
            return jsonify({"cityList" : citys, "cityData": retDict})
    except:
        pass

# return_dict = extract_summary(couch, summary_db)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)




# Qianjun Ding 1080391
# Zhiyuan Gao 1068184
# Jiachen Li 1068299
# Yanting Mu 1068314
# Chi Zhang 1067750

import queue
from flask import Flask, jsonify, request, make_response, send_file
from flask_cors import CORS
from readSummary import extract_summary
from couchdb import Server


# Initialise

DB_USERNAME = "admin"
DB_PASSWORD = "admin"
couch = Server()
couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)

# Gateway backend following ReSTful
app = Flask(__name__, static_url_path="")
CORS(app)

# scenario dictionary
scenarioDict = dict()

tasks = [{"name": "aurin_preserve",
          "type": "preserve",
          "task": "aurin"},
         {"name": "historic_preserve",
          "type": "preserve",
          "task": "historic"},
         {"name": "aurin_payroll",
          "type": "aurin",
          "keyword": "payroll",
          "level": "sa3",
          "prerequisite": "aurin_preserve"},
         {"name": "aurin_income",
          "type": "aurin",
          "keyword": "income",
          "level": "sa3",
          "prerequisite": "aurin_preserve"},
         {"name": "aurin_immigration",
          "type": "aurin",
          "keyword": "immigration",
          "level": "city",
          "prerequisite": "aurin_preserve"},
         {"name": "aurin_salary",
          "type": "aurin",
          "keyword": "salary",
          "level": "city",
          "prerequisite": "aurin_preserve"},
         {"name": "search_election",
          "type": "search",
          "keyword": "Election"},
         {"name": "search_crime",
          "type": "search",
          "keyword": "crime"},
         {"name": "historic_crime",
          "type": "historic",
          "keyword": "crime",
          "prerequisite": "historic_preserve"},
         {"name": "historic_all",
          "type": "historic",
          "keyword": "all",
          "prerequisite": "historic_preserve"}]


scenarioDict["Income (sa3) VS overall sentiment"] = [
    {"name": "aurin_income", "level": "sa3"}, {"name": "historic_all", "method": "sentiment"}]
scenarioDict["Income (city) VS attitude toward election"] = [
    {"name": "aurin_salary", "level": "city"}, {"name": "search_election", "method": "sentiment"}]
scenarioDict["Income (city) VS count of mentioning crime"] = [
    {"name": "aurin_salary", "level": "city"}, {"name": "search_crime", "method": "count"}]
scenarioDict["Crime count (sa3)"] = [
    {"name": "historic_crime", "method": "count"}]
scenarioDict["Income (city) VS election count"] = [
    {"name": "aurin_salary", "level": "city"}, {"name": "search_election", "method": "count"}]


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
        couch.delete("pending")
        pending = couch.create('pending')
    try:
        working = couch.create('working')
    except:
        couch.delete("working")
        working = couch.create('working')

    try:
        finished = couch.create('finished')
    except:
        couch.delete("finished")
        finished = couch.create('finished')
    for t in tasks:
        if t['name'] not in pending:
            t['_id'] = t['name']
            t['state'] = 'pending'
            pending.save(t)
    return {"status": "success"}, 200


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
    return {"status": "success"}, 200


def get_pending():
    return list(pending)


def get_working():
    return list(working)


def get_finished():
    return list(finished)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


##### Front end serving #####
# Serve the static file to client's browser

# print(scenarioDict.keys())
# get all task names with "city" or "sa3" on its second section
def getCoord(city):
    cityDict = {
        "Melbourne": [-37.840935, 144.946457],
        "Sydney": [-33.865143, 151.209900],
        "Canberra": [-35.282001, 149.128998],
        "Brisbane": [-27.470125, 153.021072],
        "Perth": [-31.953512, 115.857048],
        "Adelaide": [-34.846111, 138.503052],
        "Hobart": [-42.880554, 147.324997],
        "Darwin": [-12.462827, 130.841782]
    }
    print("city is ====>" + city)
    return cityDict[city]


def getAurinTasksName(scale):
    tasks = []
    for name in couch:
        try:
            if (str(name).split('_'))[1] == scale:
                tasks.append(name)
        except:
            pass
    return tasks


def translateDBString2stdTask(nameDB):
    try:
        items = nameDB.split("_")
        if items[0] == "aurin":
            ret = {"name": "aurin_" + items[2],
                   "type": "aurin",
                   "keyword": items[2],
                   "level": items[1],
                   "prerequisite": "aurin_preserve"
                   }
        if items[0] == "historic":
            ret = {"name": "historic_" + items[1],
                   "type": "historic",
                   "keyword": items[1],
                   "level": "sa3",
                   "prerequisite": "historic_preserve",
                   }
            if len(items) >= 4:
                ret["method"] = items[3]
        if items[0] == "search":
            ret = {"name": "search_" + items[1],
                   "type": "search",
                   "keyword": items[1],
                   "level": "city",
                   }
            if len(items) >= 4:
                ret["method"] = items[3]
    except:
        ret = None
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
    return {"status": "success"}, 200


@app.route("/add_task_working")
def add_task_working():
    task = request.json
    task['_id'] = task["name"]
    working.save(task)
    return {"status": "success"}, 200


@app.route("/add_task_finished")
def add_task_finished():
    task = request.json
    task['_id'] = task["name"]
    finished.save(task)
    return {"status": "success"}, 200

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
        print("testing scenario: " + scenario)
        flag = True
        for task in scenarioDict[scenario]:
            print(task["name"])
            if not check_finished(task["name"]):
                flag = False
        if flag:
            availableScenarios.append(scenario)
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


@app.route('/static/media/<filename>', methods=["GET"])
def get_media(filename):
    return send_file('./instance/static/media/{0}'.format(filename))


@app.route('/favicon.ico', methods=["GET"])
def get_ico():
    return send_file('./instance/favicon.ico')


@app.route('/app/<foo>', methods=["GET"])
def serve(foo):
    return send_file('./instance/index.html')

# handel requests from page "submit"
@app.route('/request/submit', methods=['GET', 'POST'])
def submit_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "preCalculatedList_SA3":
            print(getAurinTasksName("sa3"))
            return jsonify({"preCalculatedList": getAurinTasksName("sa3")})
        if json_data["request"] == "preCalculatedList_City":
            print(getAurinTasksName("city"))
            return jsonify({"preCalculatedList": getAurinTasksName("city")})
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
                task_0 = translateDBString2stdTask(json_data['0-0-preCal'])
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
                    task_1 = translateDBString2stdTask(json_data['0-1-preCal'])
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
            return jsonify({"state": "success"})
    except:
        print("something wrong")
        return jsonify({"state": "failed"})

# handel requests from page "submit"
@app.route('/request/plot', methods=['GET', 'POST'])
def plot_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "plotList":
            print(getScenarioAvailable())
            return jsonify({"plotList": getScenarioAvailable()})
        if json_data["request"] == "getData":
            scenarioRequested = json_data["scenario"]
            if len(scenarioDict[scenarioRequested]) == 1:
                raw = extract_summary(
                    couch, scenarioDict[scenarioRequested][0])
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
                data_0 = extract_summary(
                    couch, scenarioDict[scenarioRequested][0])
                data_1 = extract_summary(
                    couch, scenarioDict[scenarioRequested][1])
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
        return jsonify({"state": "failed"})

# replace and delete this thing
def get_city_db():
    res = []
    for d in couch:
        d_list = d.split('_')
        if len(d_list) >= 3 and d_list[-1] == 'summary' and d_list[1] == "city":
            res.append(d+"_count")
            res.append(d+"_sentiment")
    return res

###########################


@app.route('/request/map', methods=['GET', 'POST'])
def map_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "dataList":
            return jsonify({"dataList": list(get_city_db())})
            # return jsonify({"dataList" : ["kangaroo beat human(count)", "kangaroo beat human(count) VS human beat kangaroo(count)"]})
        if json_data["request"] == "cityData":
            print("request data: " + json_data["scenario"])
            datadict = extract_summary(
                couch, translateDBString2stdTask(json_data["scenario"]))
            retDict = dict()
            print("datadict ")
            print(datadict)
            for name in datadict.keys():
                print(name)
                retDict[name] = [getCoord(name), datadict[name]]
            citys = list(datadict.keys())
            print({"cityList": citys, "cityData": retDict})
            return jsonify({"cityList": citys, "cityData": retDict}), 200
    except Exception as e:
        print(e)
        pass


# return_dict = extract_summary(couch, summary_db)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)

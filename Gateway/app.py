import queue, datetime
from flask import Flask, jsonify, request, make_response, send_file
from flask_cors import CORS
from datetime import timedelta
from readSummary import extract_summary

from couchdb import Server


# Initialise

DB_USERNAME= "admin"
DB_PASSWORD= "admin"
couch = Server()
couch.resource.credentials = (DB_USERNAME, DB_PASSWORD)

# 牟老师
# return_dict = extract_summary(couch, summary_db)


# Gateway backend following ReSTful
app = Flask(__name__, static_url_path="")
CORS(app)

queueing_task = queue.Queue()
# (due date, task, worker IP)
working_task = []
finished_task = []
timeout = timedelta(days=1)


'''
example for task json:

{   "name": "aurin_income",
    "type": "aurin",
    "keyword": "income",
    "level" : "sa3" (# another level is "city")
}

example for search json:
{
    "id": "search_Election",
    "type": "search",
    "keyword": "Election",
    "city_set":["Melbourne", "Sydney", "Brisbane"]
}

example for historic json
{
    "id": "historic_Covid",
    "type": "historic",
    "keyword": "Covid",
}

'''

# @app.route('/check_task/<task_name>')
# def check_task(task_name):

# for i in range(1,20):
#     task = {"id":i, "type":"wait", "time":i}
#     queueing_task.put(task)

preserve_task_1 = {"name": "aurin_preserve", 
                "type" : "preserve",
                "task" : "aurin"
}

preserve_task_2 = {"name": "historic_preserve", 
                "type" : "preserve",
                "task" : "historic"
}

example_task_1 = {"name": "aurin_payroll",
                "type": "aurin",
                "keyword": "payroll",
                "level" : "sa3",
                "prerequisite":"aurin_preserve"
}

example_task_2 = {"name": "aurin_income",
                "type": "aurin",
                "keyword": "income",
                "level" : "sa3",
                "prerequisite":"aurin_preserve"
}

example_task_3 = {"name": "aurin_immigration",
                "type": "aurin",
                "keyword": "immigration",
                "level" : "city",
                "prerequisite":"aurin_preserve"
}

example_task_4 = {"name": "aurin_salary",
                "type": "aurin",
                "keyword": "salary",
                "level" : "city",
                "prerequisite":"aurin_preserve"
}

example_task_5 = {"name": "search_election",
                "type": "search",
                "keyword": "Election",
}

example_task_6 = {"name": "search_crime",
                "type": "search",
                "keyword": "crime",
}

example_task_7 = {"name": "historic_crime",
                "type": "historic",
                "keyword": "crime",
                "prerequisite":"historic_preserve"
}

example_task_8 = {"name": "historic_all",
                "type": "historic",
                "keyword": "all",
                "prerequisite":"historic_preserve"
}


queueing_task.put(example_task_1)
queueing_task.put(example_task_2)
queueing_task.put(example_task_3)
queueing_task.put(example_task_4)
queueing_task.put(example_task_5)
queueing_task.put(example_task_6)
queueing_task.put(example_task_7)
queueing_task.put(example_task_8)
queueing_task.put(preserve_task_1)
queueing_task.put(preserve_task_2)
# working pool

@app.route('/get_task', methods=['POST'])
def get_task():
    # print(working_task)
    json_data = request.json
    worker_ip = str(json_data.get("worker_ip"))
    if working_task and working_task[0][0] < datetime.datetime.now():
        task = working_task.pop()[1]
        working_task.append((datetime.datetime.now()+timeout,task, worker_ip))
        return {"status":"success", "task":task}
    # take task from task queue
    if queueing_task.empty():
        print("no work")
        return {"status":"no_work"}
    task = queueing_task.get()
    prerequisite = task.get("prerequisite", None)
    limit = queueing_task.qsize()
    index = 0
    while prerequisite not in finished_task and prerequisite != None:
        if index > limit:
            print("No fulfilled task")
            return {"status":"no prerequisite fulfilled task"}
        print(f"prerequisite {prerequisite} not fulfilled for task "+str(task.get("name")))
        queueing_task.put(task)
        task = queueing_task.get()
        prerequisite = task.get("prerequisite", None)
        index += 1
    print("Task " + str(task["name"]) + " got by worker " + worker_ip)
    working_task.append((datetime.datetime.now()+timeout,task, worker_ip))
    return {"status":"success", "task":task}


@app.route('/finish_task', methods=['POST'])
def finish_task():
    # print(working_task)
    json_data = request.json
    task_name = json_data.get('task_name', "nameless task")
    if task_name in finished_task:
        return {"status":"success"}, 200
    print("Finish " + str(task_name))
    flag = False
    for t in working_task:
        if t[1].get("name", None) == task_name:
            working_task.remove(t)
            flag = True
            break
    if flag:
        finished_task.append(task_name)
    return {"status":"success"}, 200

        
@app.route('/failed_task', methods=['POST'])
def failed_task():
    json_data = request.json
    task_name = json_data.get('task_name', "nameless task")
    if task_name in finished_task:
        return {"status":"success"}, 200
    print("Failed " + str(task_name))
    for t in working_task:
        if t[1].get("name", None) == task_name:
            temp = t
            working_task.remove(t)
            working_task.insert(0, (datetime.datetime.now(), temp[1], temp[2]))
            break
    return {"status":"success"}, 200
        
# Front end
@app.route('/queueing_task', methods=['GET'])
def get_queueing_task():
    return str(queueing_task)

@app.route('/finished_task', methods=['GET'])
def get_finished_task():
    return str(finished_task)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


##### Front end serving #####
# Serve the static file to client's browser
@app.route('/', methods=["GET"])
def get_index():
    return send_file('./instance/index.html')

@app.route('/static/js/<filename>', methods=["GET"])
def get_js(filename):
    return send_file('./instance/static/js/{0}'.format(filename))

@app.route('/static/css/<filename>', methods=["GET"])
def get_css(filename):
    return send_file('./instance/static/css/{0}'.format(filename))

# Save for future use
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

@app.route('/request/submit', methods = ['GET', 'POST'])
def submit_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "preCalculatedList_SA3":
            return jsonify({"preCalculatedList" : ["kangaroo beat human count SA3", "human beat kangaroo count"]})
        if json_data["request"] == "preCalculatedList_City":
            return jsonify({"preCalculatedList" : ["kangaroo beat human count City", "human eat kangaroo count"]})
    except:
        pass

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
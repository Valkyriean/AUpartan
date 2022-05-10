"""
Original Source Code:
https://gist.github.com/miguelgrinberg/5614326

This is a simple Flask CRUD application to manage Task entities.
"""

import queue
from flask import Flask, jsonify, abort, request, make_response, url_for, send_file
from flask_cors import CORS

# Gateway backend following ReSTful
app = Flask(__name__, static_url_path="")
CORS(app)

queueing_task = queue.Queue()
working_task = []
finished_task = []

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

example_task = {"name": "aurin_payroll",
                "type": "aurin",
                "keyword": "payroll",
                "level" : "sa3"
}

example_task_2 = {"name": "search_election",
                "type": "search",
                "keyword": "Election",
}

example_task_3 = {"name": "historic_heart",
                "type": "historic",
                "keyword": "heart",
}

queueing_task.put(preserve_task_1)
queueing_task.put(preserve_task_2)
queueing_task.put(example_task)
queueing_task.put(example_task_2)
# queueing_task.put(example_task_2)
# working pool

@app.route('/get_task', methods=['POST'])
def get_task():
    json_data = request.json
    print(json_data)
    if queueing_task.empty():
        return {"status":"no_work"}
    task = queueing_task.get()
    print("Task " + str(task["name"]) + " got by worker " + str(json_data['worker_id']))
    working_task.append(task)
    return {"status":"success", "task":task}


@app.route('/finish_task', methods=['POST'])
def finsh_task():
    json_data = request.json
    task_name = json_data['task_name']
    print("Finish " + str(task_name))
    finished_task.append(task_name)
    return "Success", 200

        
@app.route('/failed_task', methods=['POST'])
def failed_task():
    json_data = request.json
    task_name = json_data['task_name']
    print("Failed " + str(task_name))
    # finished_task.append(task_name)
    return "Success", 200
        
# Front end
@app.route('/queueing_task', methods=['GET'])
def get_queueing_task():
    return str(queueing_task)

@app.route('/finished_task', methods=['GET'])
def get_finished_task():
    return str(finished_task)
        
# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]

# def make_public_task(task):
#     new_task = {}
#     for field in task:
#         if field == 'id':
#             new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
#         else:
#             new_task[field] = task[field]
#     return new_task



    


# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': list(map(make_public_task, tasks))})


# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = list(filter(lambda t: t['id'] == task_id, tasks))
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': make_public_task(task[0])})


# @app.route('/todo/api/v1.0/tasks', methods=['POST'])
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': make_public_task(task)}), 201


# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
#     task = list(filter(lambda t: t['id'] == task_id, tasks))
#     if len(task) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'title' in request.json and type(request.json['title']) != str:
#         abort(400)
#     if 'description' in request.json and type(request.json['description']) is not str:
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description', task[0]['description'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     return jsonify({'task': make_public_task(task[0])})


# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
# def delete_task(task_id):
#     task = list(filter(lambda t: t['id'] == task_id, tasks))
#     if len(task) == 0:
#         abort(404)
#     tasks.remove(task[0])
#     return jsonify({'result': True})


@app.errorhandler(400)
def bad_resuest(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


##### back end for front end here #####
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

#no image yet
@app.route('/img/<filename>', methods=["GET"])
def get_img(filename):
    return send_file('./static/dist/img/{0}'.format(filename))

#no media yet
@app.route('/media/<filename>', methods=["GET"])
def get_media(filename):
    return send_file('./static/dist/media/{0}'.format(filename))

@app.route('/favicon.ico', methods=["GET"])
def get_ico():
    return send_file('./instance/favicon.ico')

# @app.route('/app', methods=["GET"])
# def serve1():
#     return send_file('./instance/index.html')

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
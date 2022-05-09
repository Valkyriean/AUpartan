"""
Original Source Code:
https://gist.github.com/miguelgrinberg/5614326

This is a simple Flask CRUD application to manage Task entities.
"""

import queue
from flask import Flask, jsonify, abort, request, make_response, url_for




# Gateway backend following ReSTful
app = Flask(__name__, static_url_path="")




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

example_task = {"name": "aurin_payroll",
                "type": "aurin",
                "keyword": "payroll",
                "level" : "sa3"
}

example_task_2 = {"name": "search_covid",
                "type": "search",
                "keyword": "covid",
                "city_set" : ["Canberra", "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Hobart"]
}

example_task_3 = {"name": "historic_heart",
                "type": "historic",
                "keyword": "heart",
}

queueing_task.put(example_task)
queueing_task.put(example_task_2)
queueing_task.put(example_task_3)

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

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=3000)

from os import system
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/map', methods = ['GET', 'POST'])
def map_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "dataList":
            return jsonify({"dataList" : ["kangaroo beat human(count)", "kangaroo beat human(count) VS human beat kangaroo(count)"]})
        if json_data["request"] == "data":
            sumCoord = json_data["lng"] + json_data["lat"]      # replace with true result
            return jsonify({"sum" : str(json_data["lng"]) + "   " + str(json_data["lat"])})             # replace with standard json
    except:
        pass

@app.route('/request/submit', methods = ['GET', 'POST'])
def submit_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "preCalculatedList_SA3":
            print("lalalalala")
            return jsonify({"preCalculatedList" : ["kangaroo beat human count SA3", "human beat kangaroo count"]})
        if json_data["request"] == "preCalculatedList_City":
            print("lalalalala")
            return jsonify({"preCalculatedList" : ["kangaroo beat human count City", "human eat kangaroo count"]})
        if json_data["request"] == "task":
            print("lalalalala")
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
                task_0 = {
                    'name': taskType + '_' + json_data['0-0-preCal'],
                    'type': taskType,
                    'keyword': json_data['0-0-preCal'],
                    'level': json_data['scale']
                }
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
                    task_1 = {
                        'name': taskType + '_' + json_data['0-1-preCal'],
                        'type': taskType,
                        'keyword': json_data['0-1-preCal'],
                        'level': json_data['scale']
                    }
                print({scenarioName: [task_0, task_1]})
                ##### add scenario {scenarioName: [task_0, task_1]} #####
                ##### add task set(task_0, task_1) #####
            else:
                print({scenarioName: [task_0]})
                ##### add scenario {scenarioName: [task_0]} #####
                ##### add task set(task_0) #####
                pass 
            return jsonify({"state" : "success"})
    except:
        print("something wrong")
        return jsonify({"state" : "failed"})
        


# task = {"name": "aurin_payroll",
#                 "type": "aurin",
#                 "keyword": "payroll",
#                 "level" : "sa3"
# }

# example_task_2 = {"name": "search_election",
#                 "type": "search",
#                 "keyword": "Election",
# }
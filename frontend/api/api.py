from os import system
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

@app.route('/request/map', methods = ['GET', 'POST'])
def map_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "dataList":
            return jsonify({"dataList" : ["kangaroo beat human(count)", "kangaroo beat human(count) VS human beat kangaroo(count)"]})
        if json_data["request"] == "cityData":
            print("request data: " + json_data["scenario"])
            datadict = {"Melbourne": 1999, "Canberra": 9990, "Sydney": 2990}
            retDict = dict()
            for name in datadict.keys():
                print(name)
                retDict[name] = [getCoord(name), datadict[name]]
            citys = list(datadict.keys())
            print({"cityList" : citys, "cityData": retDict})
            return jsonify({"cityList" : citys, "cityData": retDict})
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
        
# handel requests from page "submit"
@app.route('/request/plot', methods = ['GET', 'POST'])
def plot_communication():
    try:
        json_data = request.json
        print(json_data)
        if json_data["request"] == "plotList":
            return jsonify({"plotList" : ["a", "abc"]})
        if json_data["request"] == "getData":
            scenarioRequested = json_data["scenario"]
            if len(scenarioRequested) == 1:
                raw = {"abc": 1, "23bcd4": 2, "def": 3}
                keys = []
                y = []
                for key in raw.keys():
                    keys.append(key)
                    y.append(raw[key])
                return jsonify({"data": {"type": "bar", "x": keys, "y": y}, "titleLabel": "lalala", "xLabel": "xxxx", "yLabel": "yyyyy"})
            else:
                data_0 = {"abc": 11, "bcd": 12, "def": 13}
                data_1 = {"bcd": 222, "def": 333, "efg": 444}
                x = []
                y = []
                keys = []
                for key in data_0.keys():
                    if key in data_1.keys():
                        x.append(data_0[key])
                        y.append(data_1[key])
                        keys.append(key)
                return jsonify({"data": {"type": "scatter", "mode": "markers", "x": x, "y": y, "text": keys}, "titleLabel": "lalala", "xLabel": "xxxx", "yLabel": "yyyyy"})

    except:
        print("something wrong")
        return jsonify({"state" : "failed"})
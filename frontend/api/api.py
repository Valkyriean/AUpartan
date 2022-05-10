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
            return jsonify({"preCalculatedList" : ["kangaroo beat human count SA3", "human beat kangaroo count"]})
        if json_data["request"] == "preCalculatedList_City":
            return jsonify({"preCalculatedList" : ["kangaroo beat human count City", "human eat kangaroo count"]})
    except:
        pass
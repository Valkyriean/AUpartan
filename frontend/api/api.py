from os import system
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/map', methods = ['GET', 'POST'])
def get_map_string():
    json_data = request.json
    sumCoord = json_data["lng"] + json_data["lat"]
    return jsonify({"sum" : str(sumCoord)})
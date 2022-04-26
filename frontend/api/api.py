from os import system
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/map', methods = ['POST'])
def get_map_string():
    json_data = request.json
    sumCoord = json_data["long"] + json_data["lat"]
    return {'sum': sumCoord} 
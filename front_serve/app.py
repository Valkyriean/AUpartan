from flask import Flask, send_file
from flask_cors import CORS
from flask import  request, jsonify

app = Flask(__name__)
CORS(app)

# Serve the static file to client's browser
@app.route('/', methods=["GET"])
def get_index():
    return send_file('./build/index.html')

@app.route('/static/js/<filename>', methods=["GET"])
def get_js(filename):
    return send_file('./build/static/js/{0}'.format(filename))

@app.route('/static/css/<filename>', methods=["GET"])
def get_css(filename):
    return send_file('./build/static/css/{0}'.format(filename))

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
    return send_file('./build/favicon.ico')

# @app.route('/app', methods=["GET"])
# def serve1():
#     return send_file('./build/index.html')

@app.route('/app/<foo>', methods=["GET"])
def serve(foo):
    return send_file('./build/index.html')

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
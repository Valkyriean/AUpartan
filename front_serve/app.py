from flask import Flask, send_file
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Serve the static file to client's browser
@app.route('/', methods=["GET"])
def get_index():
    return send_file('./static/dist/index.html')

@app.route('/js/<filename>', methods=["GET"])
def get_js(filename):
    return send_file('./static/dist/js/{0}'.format(filename))

@app.route('/css/<filename>', methods=["GET"])
def get_css(filename):
    return send_file('./static/dist/css/{0}'.format(filename))

@app.route('/img/<filename>', methods=["GET"])
def get_img(filename):
    return send_file('./static/dist/img/{0}'.format(filename))

@app.route('/media/<filename>', methods=["GET"])
def get_media(filename):
    return send_file('./static/dist/media/{0}'.format(filename))

@app.route('/favicon.ico', methods=["GET"])
def get_ico():
    return send_file('./static/dist/favicon.ico')

@app.route('/app/<foo>', methods=["GET"])
def serve(foo):
    return send_file('./static/dist/index.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
from flask import Flask, request, jsonify, render_template
import json, os
from SubjectContext import *
app = Flask(__name__)
subject = None

#trying to get everything working on the home page
#for now, results display on a second page
@app.route('/')
def home_page():
    return app.send_static_file("main.html")

#For use by standalone web app

@app.route('/<param>')
def post_results(param):
    topic = param[:param.index('-')]
    word = param[param.index('-') + 1:]
    context = SubjectContext(topic)
    syn = context.get(word)
    return render_template("result.html", topic=topic, word=word, primary=json.dumps(syn[0]), secondary = json.dumps(syn[1]))


class InvalidUsage(Exception):
    status_code = 403

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))

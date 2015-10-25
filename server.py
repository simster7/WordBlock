from flask import Flask, request, jsonify, render_template
import json, os
from SubjectContext import *
app = Flask(__name__)
subject = None

#trying to get everything working on the home page
#for now, results display on a second page
@app.route('/')
def home_page():
    return app.send_static_file("index.html")

#For use by standalone web app
@app.route('/results', methods=['POST'])
def post_results():
    topic = request.form["topic"]
    word = request.form["word"]
    context = SubjectContext(topic)
    syn = context.get(word)
    return render_template("result.html", topic=topic, word=word, primary=json.dumps(syn[0]), secondary = json.dumps(syn[1]))

#For use by Docs plugin
@app.route('/setsubject', methods=['POST'])
def set_subject():
    arg = request.form['subject']
    subject = SubjectContext(arg)
    return "Subject set: "+arg

#For use by Docs plugin
@app.route('/getquery', methods=['GET'])
def find_synonyms():
    print(subject)
    word = request.args['word']
    if subject:
        return json.dumps(subject.get(word))
    else:
        raise InvalidUsage("Subject not yet defined. ")

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
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
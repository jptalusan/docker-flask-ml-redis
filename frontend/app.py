from flask import Flask
import os
import uuid
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory
import requests
import json
import redis
from rq import Queue, Connection
from classify_array import classify
 
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

redis_url = os.getenv('REDISTOGO_URL', 'redis://redis:6379')
conn = redis.from_url(redis_url)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/long_request')
def long_request():
    resp = ''
    with Connection(conn):
        q = Queue()
        task = q.enqueue(classify)
            
    print(task.get_id())
    return jsonify(task.get_id()), 202

@app.route('/test_request')
def test_request():
    uri = "http://163.221.68.242:8081/classify?f1=5.1&f2=3.5&f3=1.4&f4=0.2"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"  
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
   
    hostname = os.uname()[1]
    randomid = uuid.uuid4()
    
    return Jresponse + ':' + hostname + ', UUID:' + str(randomid) + '\n'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/test')
def index():
    hostname = os.uname()[1]
    randomid = uuid.uuid4()
    return 'Container Hostname: ' + hostname + ' , ' + 'UUID: ' + str(randomid) + '\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5098)

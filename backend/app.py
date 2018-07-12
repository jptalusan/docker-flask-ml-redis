from flask import Flask, jsonify, request
from sklearn import svm
from sklearn import datasets
from sklearn.externals import joblib
import numpy as np
import pandas as pd
import os
import redis
from rq import Worker, Queue, Connection
from flask.cli import FlaskGroup

HOST = '0.0.0.0'
PORT = 8081

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/testing')
def testing():
    return 'Hello world!'

@app.route('/classify')
def classify():
    f1 = request.args.get('f1')
    f2 = request.args.get('f2')
    f3 = request.args.get('f3')
    f4 = request.args.get('f4')
    
    n = np.array([[f1, f2, f3, f4]])
    n = n.astype(np.float32)

    print(n)
    
    hostname = os.uname()[1]

    clf = joblib.load('model.pkl')
    prob = clf.predict_proba(n)
    print(prob)

    count = get_hit_count()

    return jsonify(probability=prob.tolist(), hostname=hostname, count=count)
    
@app.route('/api/train', methods=['POST'])
def train():
    parameters = request.get_json()

    iris = datasets.load_iris()
    X, y = iris.data, iris.target

    clf = svm.SVC(C=float(parameters['C']),
                  probability=True,
                  random_state=1)
    clf.fit(X, y)
    joblib.dump(clf, 'model.pkl')

    return jsonify({'accuracy': round(clf.score(X, y) * 100, 2)})

if __name__ == '__main__':
    app.run(host=HOST, debug=True, port=PORT)

import redis
from rq import Worker, Connection
import os
from flask import Flask

REDIS_URL = 'redis://redis:6379/0'
QUEUES = ['default']

app = Flask(__name__)

@app.cli.command()
def runworker():
    print("running worker!")
    with Connection(redis_connection):
        worker = Worker(QUEUES)
        worker.work()


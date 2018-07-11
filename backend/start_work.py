import redis
from rq import Worker, Connection
import os

REDIS_URL = 'redis://redis:6379/0'
QUEUES = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://redis:6379')
conn = redis.from_url(redis_url)

def runworker():
    print("running worker!")
    with Connection(conn):
        worker = Worker(QUEUES)
        worker.work()

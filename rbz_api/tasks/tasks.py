import os
import time

from celery import Celery
from celery.task import Task
from rbz_api.engine.connections import send_request_to_movie_engine
from rbz_api.settings import RABBIT_PORT, RABBIT_HOST
from rbz_api.database.db_functions import set_response

## Broker settings.
BROKER_URL = u'amqp://guest:guest@{addr}:{port}//'.format(
    addr=RABBIT_HOST,
    port=RABBIT_PORT,
)

celery_app = Celery('tasks', backend='amqp', broker=BROKER_URL)

class CalculateAndSaveResponse(Task):
    queue = 'movies'

    def run(self, id, request, onesignal_id):
        print("sent request")
        result = send_request_to_movie_engine(request)
        return result

    def on_success(self, retval, task_id, args, kwargs):
        print('SUCCESS')
        set_response(args[0], retval, True, args[2])

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("ERROR: No Response calculated!")



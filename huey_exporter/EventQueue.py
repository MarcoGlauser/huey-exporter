import re

from huey import RedisHuey
from huey.consumer import EVENT_FINISHED, EVENT_STARTED, EVENT_ERROR_TASK
from prometheus_client import Summary, Counter
from huey_exporter.RedisEnqueuedEventHuey import EVENT_ENQUEUED

# Create a metric to track time spent and requests made.
ENQUEUED_COUNTER = Counter('huey_enqueued_tasks', 'Huey Tasks enqueued', ['queue_name', 'task_name'])
STARTED_COUNTER = Counter('huey_started_tasks', 'Huey Tasks started', ['queue_name', 'task_name'])
FINISHED_COUNTER = Counter('huey_finished_tasks', 'Huey Tasks Finished', ['queue_name', 'task_name'])
ERROR_COUNTER = Counter('huey_error_tasks', 'Huey Task Errors', ['queue_name', 'task_name'])
TASK_DURATION_SUMMARY = Summary('huey_task_duration_seconds', 'Time spent processing tasks', ['queue_name', 'task_name'])


class EventQueue:

    prefix = 'queue_task_'

    def __init__(self, name, connection_pool):
        self.name = name
        self.clean_name = self.clean_queue_name(self.name)
        self.huey = RedisHuey(self.name, connection_pool=connection_pool)
        self.event_handlers = {
            EVENT_FINISHED: self.event_finished,
            EVENT_ENQUEUED: self.event_enqueued,
            EVENT_STARTED: self.event_started,
            EVENT_ERROR_TASK: self.event_error,
        }

    def listen(self):
        for event in self.huey.storage:
            try:
                event_handler = self.event_handlers[event['status']]
                event_handler(event)
            except KeyError:
                print('Ignored event {status}'.format(status=event['status']))

    def event_enqueued(self, event):
        ENQUEUED_COUNTER.labels(**self.labels(event)).inc()

    def event_started(self, event):
        STARTED_COUNTER.labels(**self.labels(event)).inc()

    def event_finished(self, event):
        FINISHED_COUNTER.labels(**self.labels(event)).inc()
        TASK_DURATION_SUMMARY.labels(**self.labels(event)).observe(event['duration'])

    def event_error(self, event):
        ERROR_COUNTER.labels(**self.labels(event)).inc()

    def labels(self, event):
        return {
            'queue_name': self.name,
            'task_name': self.clean_event_name(event['task'])
        }

    def clean_event_name(self, name):
        return name[len(self.prefix):]

    # Copied from https://github.com/coleifer/huey/blob/1.9.1/huey/storage.py#L302
    def clean_queue_name(self, name):
        return re.sub('[^a-z0-9]', '', name)

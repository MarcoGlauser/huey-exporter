import re

from huey import RedisHuey
from huey.consumer import EVENT_FINISHED, EVENT_STARTED, EVENT_ERROR_TASK
from prometheus_client import Summary, Counter

# Create a metric to track time spent and requests made.
STARTED_COUNTER = Counter('huey_started_tasks', 'Huey Tasks started', ['task_name'])
FINISHED_COUNTER = Counter('huey_finished_tasks', 'Huey Tasks Finished', ['task_name'])
ERROR_COUNTER = Counter('huey_error_tasks', 'Huey Task Errors', ['task_name'])
TASK_DURATION_SUMMARY = Summary('huey_task_duration_seconds', 'Time spent processing tasks', ['task_name'])


class EventQueue:

    prefix = 'queue_task_'

    def __init__(self, name, connection_pool):
        self.name = self.clean_queue_name(name)
        self.huey = RedisHuey(name, connection_pool=connection_pool)

    def listen(self):
        for event in self.huey.storage:
            if event['status'] == EVENT_FINISHED:
                self.event_finished(event)
            elif event['status'] == EVENT_STARTED:
                self.event_started(event)
            elif event['status'] == EVENT_ERROR_TASK:
                self.event_error(event)

    def event_started(self, event):
        STARTED_COUNTER.labels(**self.labels(event)).inc()

    def event_finished(self, event):
        FINISHED_COUNTER.labels(**self.labels(event)).inc()
        TASK_DURATION_SUMMARY.labels(**self.labels(event)).observe(event['duration'])

    def event_error(self, event):
        ERROR_COUNTER.labels(**self.labels(event)).inc()

    def labels(self, event):
        return {
            'task_name': self.clean_event_name(event['task'])
        }

    def clean_event_name(self, name):
        return name[len(self.prefix):]

    # Copied from https://github.com/coleifer/huey/blob/1.9.1/huey/storage.py#L302
    def clean_queue_name(self, name):
        return re.sub('[^a-z0-9]', '', name)

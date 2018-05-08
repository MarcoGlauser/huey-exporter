from huey import RedisHuey

EVENT_ENQUEUED = 'enqueued'


class RedisEnqueuedEventHuey(RedisHuey):

    def enqueue(self, task):
        super(RedisEnqueuedEventHuey, self).enqueue(task)
        if not self.always_eager:
            self.emit_task(EVENT_ENQUEUED, task)

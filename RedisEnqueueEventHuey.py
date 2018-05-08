from huey import RedisHuey

EVENT_ENQUEUED = 'enqueued'


class RedisEnqueueEventHuey(RedisHuey):

    def enqueue(self, task):
        super(RedisEnqueueEventHuey, self).enqueue(task)
        if not self.always_eager:
            self.emit_task(EVENT_ENQUEUED, task)

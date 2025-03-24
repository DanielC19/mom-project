from src.models.queue import Queue

class QueueService:
    def __init__(self):
        self.queues = {}

    def create_queue(self, queue:Queue):
        self.queues[queue.queue_id] = queue

    def get_queues(self):
        return [queue.to_dict() for queue in self.queues.values()]

    def push_message(self, data, queue_id):
        try:
            self.queues[queue_id].enqueue(data)
            return True
        except Exception as e:
            return False

    def pull_message(self, queue_id):
        try:
            message = self.queues[queue_id].dequeue()
            return message
        except Exception as e:
            return False
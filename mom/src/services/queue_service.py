from src.models.message import Message
from src.models.queue import Queue

class QueueService:
    def __init__(self):
        self.queues = {}

    def create_queue(self, queue:Queue, autor):
        self.queues[queue["queue_id"]] = Queue(queue["queue_id"], autor)

    def get_queues(self):
        return [{"queue_id": queue.to_dict()["queue_id"], "autor": queue.to_dict()["autor"]} for queue in self.queues.values()] 

    def push_message(self, data, queue_id):
        try:
            message = Message(data["content"], parent=queue_id, sender=data["sender"])
            self.queues[queue_id].enqueue(message)
            return True
        except Exception as e:
            return False

    def pull_message(self, queue_id):
        try:
            message = self.queues[queue_id].dequeue()
            return message
        except Exception as e:
            return False
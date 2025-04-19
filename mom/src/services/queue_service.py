from src.models.message import Message
from src.models.queue import Queue
from src.utils.replication_pb2 import Message as ProtoMessage

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

    def delete_queue(self, queue_id, user):
        if queue_id in self.queues:
            queue = self.queues[queue_id]
            if queue.autor != user:  # Validar que el usuario sea el creador
                print(f"User {user} is not authorized to delete queue {queue_id}")
                return False
            del self.queues[queue_id]
            return True
        print(f"Queue {queue_id} not found")
        return False

    def get_queue_messages(self, queue_id):
        queue = self.queues.get(queue_id)
        if queue:
            return [ProtoMessage(
                        message_id=msg.message_id,
                        parent=msg.parent,
                        content=msg.content,
                        sender=msg.sender,
                        timestamp=msg.timestamp
                    ) for msg in queue.messages]
        return []
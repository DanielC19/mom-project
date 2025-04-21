from src.models.message import Message
from src.models.queue import Queue
from src.utils.mom_pb2 import MessageReplication

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

    def export_queue(self, queue_id):
        queue = self.queues[queue_id]
        if queue is not None:
            messages = [
                MessageReplication(
                    message_id=msg.to_dict().get("message_id", ""),
                    parent=msg.to_dict().get("parent", ""),
                    content=msg.to_dict().get("content", ""),
                    sender=msg.to_dict().get("sender", ""),
                    timestamp=msg.to_dict().get("timestamp", ""),
                    sent=msg.to_dict().get("sent", []),
                ) for msg in queue.messages
            ]
            data = queue.to_dict()
            data["messages"] = messages
            return data
        else:
            raise Exception(f"Queue {queue_id} not found")

    def import_queue(self, queue):
        queue_id = queue.queue_id
        if queue_id in self.queues:
            raise Exception(f"Queue {queue_id} already exists")
        else:
            self.queues[queue_id] = Queue(queue_id, queue.autor)
            for message in queue.messages:
                self.queues[queue_id].enqueue(Message(
                    message.content,
                    message.parent,
                    message.sender,
                    message_id=message.message_id,
                ))
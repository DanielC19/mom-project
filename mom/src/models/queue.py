from src.models.message import Message

class Queue:
    def __init__(self, queue_id):
        self.queue_id = queue_id
        self.messages = []

    def to_dict(self):
        return {
            'queue_id': self.queue_id,
            'messages': self.messages
        }

    def enqueue(self, message:Message):
        self.messages.append(message)

    def dequeue(self):
        return self.messages.pop(0)

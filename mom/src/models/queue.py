from src.models.message import Message

queue_schema = {
    "type": "object",
    "properties": {
        "queue_id": {"type": "string"}
    },
    "required": ["queue_id"],
}
 
class Queue:
    def __init__(self, queue_id, autor):
        self.queue_id = queue_id
        self.autor= autor
        self.messages = []

    def to_dict(self):
        return {
            'queue_id': self.queue_id,
            'autor': self.autor,
            'messages': [message.to_dict() for message in self.messages]
        }

    def enqueue(self, message:Message):
        self.messages.append(message)

    def dequeue(self):
        return self.messages.pop(0)

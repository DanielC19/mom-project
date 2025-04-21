from datetime import datetime
import random

message_schema = {
    "type": "object",
    "properties": {
        "content": {"type": "string"},
        "sender": {"type": "string"},
    },
    "required": ["content"],
}

class Message:
    def __init__(self, content, parent, sender=None,  message_id=None):
        if message_id is None:
            message_id = self.generate_message_id(parent)
        self.message_id = message_id
        self.message_id = self.generate_message_id(parent)
        self.parent = parent
        self.content = content
        self.sender = sender
        self.sent = []
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            'message_id': self.message_id,
            'parent': self.parent,
            'content': self.content,
            'sender': self.sender,
            'timestamp': self.timestamp
        }

    def generate_message_id(self, parent) -> str :
        return parent + '_' + str(random.randint(100000, 999999))
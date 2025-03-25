from datetime import datetime
import random

class Message:
    def __init__(self, content, parent, sender=None):
        self.message_id = self.generate_message_id(parent)
        self.parent = parent
        self.content = content
        self.sender = sender
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
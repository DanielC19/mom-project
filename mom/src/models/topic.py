from src.models.message import Message

topic_schema = {
    "type": "object",
    "properties": {
        "topic_id": {"type": "string"}
    },
    "required": ["topic_id"],
}

class Topic:
    def __init__(self, topic_id, autor):
        self.topic_id = topic_id
        self.autor = autor
        self.messages = []
        self.subscribers = []

    def to_dict(self):
        return {
            'topic_id': self.topic_id,
            'autor': self.autor,
            'messages': [message.to_dict() for message in self.messages]
        }

    def publish_message(self, message: Message):
        self.messages.append(message)
        
        return True

    def subscribe(self, subscriber_id):
        if subscriber_id not in self.subscribers:
            self.subscribers.append(subscriber_id)
            return True
        return False

    def unsubscribe(self, subscriber_id):
        if subscriber_id in self.subscribers:
            self.subscribers.remove(subscriber_id)
            return True
        return False

    def pull_messages(self, subscriber_id):
        messages_to_send = []
        for message in self.messages:
            if subscriber_id not in message.sent:
                messages_to_send.append(message)
                message.sent.append(subscriber_id)
        return messages_to_send
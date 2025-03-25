from src.models.message import Message

class Topic:
    def __init__(self, topic_id):
        self.topic_id = topic_id
        self.messages = []
        self.subscribers = []

    def to_dict(self):
        return {
            'topic_id': self.topic_id,
            'messages': [message.to_dict() for message in self.messages]
        }

    def publish_message(self, message:Message):
        self.messages.append(message)
        return True

    def subscribe(self, subscriber_id):
        if(subscriber_id not in self.subscribers):
            self.subscribers.append(subscriber_id)
            return True
        return False

    def unsubscribe(self, subscriber_id):
        if(subscriber_id in self.subscribers):
            self.subscribers.remove(subscriber_id)
            return True
        return False
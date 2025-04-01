from src.models.message import Message

topic_schema = {
    "type": "object",
    "properties": {
        "topic_id": {"type": "string"}
    },
    "required": ["topic_id"],
}

class Topic:
    def __init__(self, topic_id):
        self.topic_id = topic_id
        self.messages = []
        self.subscribers = {}  # Cambiado a diccionario para manejar colas por suscriptor

    def to_dict(self):
        return {
            'topic_id': self.topic_id,
            'messages': [message.to_dict() for message in self.messages]
        }

    def publish_message(self, message: Message):
        self.messages.append(message)
        for subscriber_id in self.subscribers:
            self.subscribers[subscriber_id].append(message)  # Enviar mensaje a cada suscriptor
        return True

    def subscribe(self, subscriber_id):
        if subscriber_id not in self.subscribers:
            self.subscribers[subscriber_id] = []  # Inicializa la cola del suscriptor
            return True
        return False

    def unsubscribe(self, subscriber_id):
        if subscriber_id in self.subscribers:
            del self.subscribers[subscriber_id]  # Elimina la cola del suscriptor
            return True
        return False

    def pull_messages(self, subscriber_id):
        messages_to_send = []
        for message in self.messages:
            if(subscriber_id not in message.sent):
                messages_to_send.append(message)
                message.sent.append(subscriber_id)
        return messages_to_send
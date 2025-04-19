from src.models.topic import Topic
from src.models.message import Message
from src.utils.replication_pb2 import Message as ProtoMessage  # para construir mensajes

class TopicsService:
    def __init__(self):
        self.topics = {}

    def create_topic(self, topic_id, autor):
        if topic_id not in self.topics:
            self.topics[topic_id] = Topic(topic_id, autor)
            return True
        return False

    def publish_message(self, topic_id, data):
        if topic_id in self.topics:
            message = Message(**data, parent=topic_id)
            self.topics[topic_id].publish_message(message)
            return True
        return False

    def subscribe(self, topic_id, subscriber_id):
        if topic_id in self.topics:
            return self.topics[topic_id].subscribe(subscriber_id)
        return False

    def unsubscribe(self, topic_id, subscriber_id):
        if topic_id in self.topics:
            return self.topics[topic_id].unsubscribe(subscriber_id)
        return False

    def get_topics(self):
        return [{"topic_id": topic.to_dict()["topic_id"], "autor": topic.to_dict()["autor"]} for topic in self.topics.values()]

    def pull_messages(self, topic_id, subscriber_id):
        if topic_id in self.topics:
            return self.topics[topic_id].pull_messages(subscriber_id)
        return []

    def delete_topic(self, topic_id, user):
        if topic_id in self.topics:
            topic = self.topics[topic_id]
            if topic.autor != user:  # Validar que el usuario sea el creador
                print(f"User {user} is not authorized to delete topic {topic_id}")
                return False
            del self.topics[topic_id]
            return True
        print(f"Topic {topic_id} not found")
        return False

    def get_topic_messages(self, topic_id):
        # Se simula la obtención de mensajes; se asume que cada topic almacena una lista de mensajes (objetos o dicts)
        topic = self.topics.get(topic_id)
        if topic and "messages" in topic:
            # Convertir cada mensaje a ProtoMessage; se espera que cada mensaje tenga id, parent, content, sender y timestamp
            return [ProtoMessage(
                        message_id=msg.get("message_id", ""),
                        parent=msg.get("parent", ""),
                        content=msg.get("content", ""),
                        sender=msg.get("sender", ""),
                        timestamp=msg.get("timestamp", "")
                    ) for msg in topic["messages"]]
        return []
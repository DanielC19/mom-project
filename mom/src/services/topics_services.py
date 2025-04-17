from src.models.topic import Topic
from src.models.message import Message

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

    def delete_topic(self, topic_id):
        if topic_id in self.topics:
            del self.topics[topic_id]
            return True
        return False
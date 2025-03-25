from flask import jsonify
from src.services.topics_services import TopicsService

class TopicController:
    def __init__(self):
        self.topics_service = TopicsService()

    def create_topic(self, data):
        success = self.topics_service.create_topic(data["topic_id"])
        if success:
            return jsonify({"message":"Topic created"}), 201
        return jsonify({"message":"Topic already exists"}), 400

    def publish_message(self, topic_id, data):
        success = self.topics_service.publish_message(topic_id, data)
        if success:
            return jsonify({'message': "Message published"}), 201
        return jsonify({'message': "Topic not found"}), 400

    def subscribe(self, topic_id, subscriber_id):
        success = self.topics_service.subscribe(topic_id, subscriber_id)
        if success:
            return jsonify({"message":"Subscribed successfully"}), 201
        return jsonify({"message":"Subscription failed"}), 400

    def unsubscribe(self, topic_id, subscriber_id):
        success = self.topics_service.unsubscribe(topic_id, subscriber_id)
        if success:
            return jsonify({"message":"Unsubscribed successfully"}), 201
        return jsonify({"message":"Unsubscribed failed"}), 400

    def list_topics(self):
        topics = self.topics_service.get_topics()
        return jsonify(topics), 200

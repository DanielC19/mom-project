from src.models.message import message_schema
from src.models.topic import topic_schema
from src.services.topics_services import TopicsService
from src.utils.utils import validate_input, generate_response, log_error

class TopicController:
    def __init__(self):
        self.topics_service = TopicsService()

    def create_topic(self, data):
        try:
            validate_input(data, topic_schema)
            success = self.topics_service.create_topic(data["topic_id"])
            if success:
                return generate_response(True, "Topic created"), 201
            return generate_response(False, "Topic already exists", data), 400
        except Exception as e:
            return generate_response(False, e.message, data), 400

    def publish_message(self, topic_id, data):
        try:
            validate_input(data, message_schema)
            success = self.topics_service.publish_message(topic_id, data)
            if success:
                return generate_response(True, "Message published"), 201
            return generate_response(False, "Topic not found", data), 400
        except Exception as e:
            return generate_response(False, e.message, data), 400

    def subscribe(self, topic_id, subscriber_id):
        success = self.topics_service.subscribe(topic_id, subscriber_id)
        if success:
            return generate_response(True, "Subscribed successfully"), 201
        return generate_response(False, "Subscription failed"), 400

    def unsubscribe(self, topic_id, subscriber_id):
        success = self.topics_service.unsubscribe(topic_id, subscriber_id)
        if success:
            return generate_response(True, "Unsubscribed successfully"), 201
        return generate_response(False, "Unsubscribed failed"), 400

    def list_topics(self):
        topics = self.topics_service.get_topics()
        return generate_response(True, "Topics listed", topics), 200

    def pull_messages(self, topic_id, subscriber_id):
        messages = self.topics_service.pull_messages(topic_id, subscriber_id)
        if messages:
            formatted_messages = [message.to_dict() for message in messages]
            return generate_response(True, "Pulled messages", formatted_messages), 200
        return generate_response(False, "No messages or invalid topic/subscriber"), 404

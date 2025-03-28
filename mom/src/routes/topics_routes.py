from flask import Blueprint, request
from src.controllers.topics_controller import TopicController

topic_bp = Blueprint('topic', __name__)
topic_controller = TopicController()

@topic_bp.route('/topic', methods=['POST'])
def create_topic():
    data = request.json
    return topic_controller.create_topic(data)

@topic_bp.route('/topic/<topic_id>/publish', methods=['POST'])
def publish_message(topic_id):
    data = request.json
    return topic_controller.publish_message(topic_id, data)

@topic_bp.route('/topic/<topic_id>/subscribe/<subscriber_id>', methods=['POST'])
def subscribe(topic_id, subscriber_id):
    return topic_controller.subscribe(topic_id, subscriber_id)

@topic_bp.route('/topic/<topic_id>/unsubscribe/<subscriber_id>', methods=['DELETE'])
def unsubscribe(topic_id, subscriber_id):
    return topic_controller.unsubscribe(topic_id, subscriber_id)

@topic_bp.route('/topics', methods=['GET'])
def list_topics():
    return topic_controller.list_topics()

@topic_bp.route('/topic/<topic_id>/pull/<subscriber_id>', methods=['GET'])
def pull_messages(topic_id, subscriber_id):
    return topic_controller.pull_messages(topic_id, subscriber_id)
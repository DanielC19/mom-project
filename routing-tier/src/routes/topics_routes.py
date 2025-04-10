import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Blueprint, request, jsonify
from src.services.routing_tier_service import routing_tier  # Import the global instance
from src.utils.response_utils import generate_response, log_error  # Import utility functions

topic_bp = Blueprint('topic', __name__)

@topic_bp.route('/topic', methods=['POST'])
def create_topic():
    try:
        data = request.json
        response = routing_tier.create_topic(data["topic_id"])
        return generate_response(response["success"], response["message"])
    except Exception as e:
        log_error(f"Error creating topic: {str(e)}")
        return generate_response(False, "Failed to create topic")

@topic_bp.route('/topic/<topic_id>/publish', methods=['POST'])
def publish_message(topic_id):
    try:
        data = request.json
        response = routing_tier.push_message_topic(topic_id, data)
        return generate_response(response["success"], response["message"])
    except Exception as e:
        log_error(f"Error publishing message to topic {topic_id}: {str(e)}")
        return generate_response(False, "Failed to publish message to topic")

@topic_bp.route('/topic/<topic_id>/pull/<user_id>', methods=['GET'])
def pull_messages(topic_id, user_id):
    try:
        response = routing_tier.pull_message_topic(topic_id, user_id)
        return generate_response(response["success"], response["message"], response["data"])
    except Exception as e:
        log_error(f"Error pulling message from topic {topic_id}: {str(e)}")
        return generate_response(False, "Failed to pull message from topic")

@topic_bp.route('/topics', methods=['GET'])
def list_topics():
    try:
        response = routing_tier.get_topics()  # Assuming topics are listed similarly to queues
        return generate_response(response["success"], response["message"], response["data"])
    except Exception as e:
        log_error(f"Error listing topics: {str(e)}")
        return generate_response(False, "Failed to retrieve topics")

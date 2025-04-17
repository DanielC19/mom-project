import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.routing_tier_service import routing_tier  # Import the global instance
from src.utils.response_utils import generate_response, log_error  # Import utility functions

topic_bp = Blueprint('topic', __name__)

@topic_bp.route('/topic', methods=['POST'])
@jwt_required()
def create_topic():
    try:
        current_user = get_jwt_identity()
        data = request.json
        response = routing_tier.create_topic(data["topic_id"])
        return generate_response(response["success"], response["message"])
    except Exception as e:
        log_error(f"Error creating topic: {str(e)}")
        return generate_response(False, "Failed to create topic")

@topic_bp.route('/topic/<topic_id>/publish', methods=['POST'])
@jwt_required()
def publish_message(topic_id):
    try:
        current_user = get_jwt_identity()
        data = request.json
        response = routing_tier.push_message_topic(topic_id, data)
        return generate_response(response["success"], response["message"])
    except Exception as e:
        log_error(f"Error publishing message to topic {topic_id}: {str(e)}")
        return generate_response(False, "Failed to publish message to topic")

@topic_bp.route('/topic/<topic_id>/pull/<user_id>', methods=['GET'])
@jwt_required()
def pull_messages(topic_id, user_id):
    try:
        current_user = get_jwt_identity()
        response = routing_tier.pull_message_topic(topic_id, user_id)
        return generate_response(response["success"], response["message"], response["data"])
    except Exception as e:
        log_error(f"Error pulling message from topic {topic_id}: {str(e)}")
        return generate_response(False, "Failed to pull message from topic")

@topic_bp.route('/topics', methods=['GET'])
@jwt_required()
def list_topics():
    try:
        current_user = get_jwt_identity()
        response = routing_tier.get_topics()  # Assuming topics are listed similarly to queues
        return generate_response(response["success"], response["message"], response["data"])
    except Exception as e:
        log_error(f"Error listing topics: {str(e)}")
        return generate_response(False, "Failed to retrieve topics")

@topic_bp.route('/topic/<topic_id>/subscribe/<user_id>', methods=['POST'])
@jwt_required()
def subscribe_topic(topic_id, user_id):
    try:
        current_user = get_jwt_identity()
        response = routing_tier.subscribe_topic(topic_id, user_id)
        return generate_response(response["success"], response["message"])
    except Exception as e:
        log_error(f"Error subscribing to topic {topic_id}: {str(e)}")
        return generate_response(False, "Failed to subscribe to topic")

@topic_bp.route('/topic/<topic_id>/unsubscribe/<user_id>', methods=['POST'])
@jwt_required()
def unsubscribe_topic(topic_id, user_id):
    try:
        current_user = get_jwt_identity()
        response = routing_tier.unsubscribe_topic(topic_id, user_id)
        return generate_response(response["success"], response["message"])
    except Exception as e:
        log_error(f"Error unsubscribing from topic {topic_id}: {str(e)}")
        return generate_response(False, "Failed to unsubscribe from topic")

@topic_bp.route('/topic/<topic_id>', methods=['DELETE'])
@jwt_required()
def delete_topic(topic_id):
    try:
        current_user = get_jwt_identity()
        response = routing_tier.delete_topic(topic_id)
        return generate_response(response["success"], response["message"])
    except Exception as e:
        log_error(f"Error deleting topic {topic_id}: {str(e)}")
        return generate_response(False, "Failed to delete topic")

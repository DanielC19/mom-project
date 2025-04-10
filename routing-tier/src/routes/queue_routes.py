from flask import Blueprint, request
from src.services.routing_tier_service import routing_tier  # Import the global instance
from src.utils.response_utils import generate_response, log_error  # Import utility functions

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/queue', methods=['POST'])
def create_queue():
    try:
        data = request.json
        response = routing_tier.create_queue(data["queue_id"], "queue", data)
        return generate_response(True, "Queue created successfully")
    except Exception as e:
        log_error(f"Error creating queue: {str(e)}")
        return generate_response(False, "Failed to create queue")

@queue_bp.route('/queue', methods=['GET'])
def list_queues():
    try:
        response = routing_tier.get_queues()
        return generate_response(True, "Queues retrieved successfully", response["data"])
    except Exception as e:
        log_error(f"Error listing queues: {str(e)}")
        return generate_response(False, "Failed to retrieve queues")

@queue_bp.route('/queue/<queue_id>', methods=['PUT'])
def push_message(queue_id):
    try:
        data = request.json
        response = routing_tier.push_message_queue(queue_id, data)
        return generate_response(True, "Message pushed successfully")
    except Exception as e:
        log_error(f"Error pushing message to queue {queue_id}: {str(e)}")
        return generate_response(False, "Failed to push message")

@queue_bp.route('/queue/<queue_id>', methods=['GET'])
def pull_message(queue_id):
    try:
        response = routing_tier.pull_message_queue(queue_id)
        return generate_response(True, "Message pulled successfully", response)
    except Exception as e:
        log_error(f"Error pulling message from queue {queue_id}: {str(e)}")
        return generate_response(False, "Failed to pull message")

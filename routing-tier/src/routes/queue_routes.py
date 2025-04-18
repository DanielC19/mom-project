from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.routing_tier_service import routing_tier  # Import the global instance
from src.utils.response_utils import generate_response, log_error  # Import utility functions

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/queue', methods=['POST'])
@jwt_required()
def create_queue():
    try:
        data = request.json
        user = get_jwt_identity()
        response = routing_tier.create_queue(data["queue_id"], user)
        return generate_response(**response)
    except Exception as e:
        log_error(f"Error creating queue: {str(e)}")
        return generate_response(False, "Failed to create queue")

@queue_bp.route('/queue', methods=['GET'])
@jwt_required()
def list_queues():
    try:
        response = routing_tier.get_queues()
        return generate_response(True, "Resources retrived successfully", response)
    except Exception as e:
        log_error(f"Error listing queues: {str(e)}")
        return generate_response(False, "Failed to retrieve queues")

@queue_bp.route('/queue/<queue_id>', methods=['PUT'])
@jwt_required()
def push_message(queue_id):
    try:
        data = request.json
        user = get_jwt_identity()
        response = routing_tier.push_message_queue(queue_id, data, user)
        return generate_response(**response)
    except Exception as e:
        log_error(f"Error pushing message to queue {queue_id}: {str(e)}")
        return generate_response(False, "Failed to push message")

@queue_bp.route('/queue/<queue_id>', methods=['GET'])
@jwt_required()
def pull_message(queue_id):
    try:
        response = routing_tier.pull_message_queue(queue_id)
        return generate_response(**response)
    except Exception as e:
        log_error(f"Error pulling message from queue {queue_id}: {str(e)}")
        return generate_response(False, "Failed to pull message")

@queue_bp.route('/queue/<queue_id>', methods=['DELETE'])
@jwt_required()
def delete_queue(queue_id):
    try:
        current_user = get_jwt_identity()
        response = routing_tier.delete_queue(queue_id, current_user)
        print(response)
        return generate_response(**response)
    except Exception as e:
        log_error(f"Error deleting queue {queue_id}: {str(e)}")
        return generate_response(False, "Failed to delete queue")

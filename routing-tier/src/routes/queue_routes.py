from flask import Blueprint, request, jsonify
from src.services.routing_tier_service import routing_tier  # Import the global instance

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/queue', methods=['POST'])
def create_queue():
    data = request.json
    response = routing_tier.create_queue(data["queue_id"], "queue", data)
    return jsonify(response)

@queue_bp.route('/queue', methods=['GET'])
def list_queues():
    response = routing_tier.get_queues()
    return jsonify(response)

@queue_bp.route('/queue/<queue_id>', methods=['PUT'])
def push_message(queue_id):
    data = request.json
    response = routing_tier.route_request(queue_id, f"queue/{queue_id}", method="PUT", data=data)
    return jsonify(response)

@queue_bp.route('/queue/<queue_id>', methods=['GET'])
def pull_message(queue_id):
    response = routing_tier.route_request(queue_id, f"queue/{queue_id}", method="GET")
    return jsonify(response)

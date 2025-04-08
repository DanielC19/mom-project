from flask import Blueprint, request, jsonify
from src.services.routing_tier_service import routing_tier  # Import the global instance

topic_bp = Blueprint('topic', __name__)

@topic_bp.route('/topic', methods=['POST'])
def create_topic():
    data = request.json
    response = routing_tier.create_queue(data["topic_id"], "topic", data)
    return jsonify(response)

@topic_bp.route('/topic/<topic_id>/publish', methods=['POST'])
def publish_message(topic_id):
    data = request.json
    response = routing_tier.route_request(topic_id, f"topic/{topic_id}/publish", method="POST", data=data)
    return jsonify(response)

@topic_bp.route('/topic/<topic_id>/subscribe/<subscriber_id>', methods=['POST'])
def subscribe(topic_id, subscriber_id):
    response = routing_tier.route_request(topic_id, f"topic/{topic_id}/subscribe/{subscriber_id}", method="POST")
    return jsonify(response)

@topic_bp.route('/topic/<topic_id>/unsubscribe/<subscriber_id>', methods=['DELETE'])
def unsubscribe(topic_id, subscriber_id):
    response = routing_tier.route_request(topic_id, f"topic/{topic_id}/unsubscribe/{subscriber_id}", method="DELETE")
    return jsonify(response)

@topic_bp.route('/topics', methods=['GET'])
def list_topics():
    response = routing_tier.get_queues()
    return jsonify(response)

@topic_bp.route('/topic/<topic_id>/pull/<subscriber_id>', methods=['GET'])
def pull_messages(topic_id, subscriber_id):
    response = routing_tier.route_request(topic_id, f"topic/{topic_id}/pull/{subscriber_id}", method="GET")
    return jsonify(response)

from flask import Blueprint, request, jsonify
from src.controllers.queue_controller import QueueController

queue_bp = Blueprint('queue', __name__)
queue_controller = QueueController()

@queue_bp.route('/queue/<queue_id>', methods=['PUT'])
def push_message(queue_id):
    data = request.json
    return queue_controller.push_message(data, queue_id)

@queue_bp.route('/queue/<queue_id>', methods=['GET'])
def pull_message(queue_id):
    return queue_controller.pull_message(queue_id)

@queue_bp.route('/queue', methods=['GET'])
def list_queues():
    return queue_controller.get_queues()

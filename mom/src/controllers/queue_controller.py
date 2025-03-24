from flask import request, jsonify
from src.models.queue import Queue
from src.services.queue_service import QueueService

class QueueController:
    def __init__(self):
        self.queue_service = QueueService()

    def create_queue(self, data):
        queue = Queue(data["queue_id"])
        self.queue_service.create_queue(queue)
        return jsonify(queue), 201

    def get_queues(self):
        queues = self.queue_service.get_queues()
        return jsonify(queues), 200

    def push_message(self, data, queue_id):
        message = self.queue_service.push_message(data, queue_id)
        if not message:
            return jsonify({"message": "Queue not found"}), 404
        return jsonify(message), 201

    def pull_message(self, queue_id):
        message = self.queue_service.pull_message(queue_id)
        if not message:
            return jsonify({"message": "Queue not found"}), 404
        return jsonify(message), 200




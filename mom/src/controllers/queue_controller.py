from src.models.queue import Queue, queue_schema
from src.models.message import message_schema
from src.services.queue_service import QueueService
from src.utils.utils import validate_input, generate_response, log_error

class QueueController:
    def __init__(self):
        self.queue_service = QueueService()

    def create_queue(self, data):
        try:
            validate_input(data, queue_schema)
            queue = Queue(data["queue_id"])
            self.queue_service.create_queue(queue)
            return generate_response(True, "Queue created"), 201
        except Exception as e:
            return generate_response(False, e.message, data), 400

    def get_queues(self):
        queues = self.queue_service.get_queues()
        return generate_response(True, "Queues listed", queues), 200

    def push_message(self, data, queue_id):
        try:
            validate_input(data, message_schema)
            response = self.queue_service.push_message(data, queue_id)
            if not response:
                return generate_response(False, "Queue not found"), 404
            return generate_response(True, "Message pushed", response), 201
        except Exception as e:
            return generate_response(False, e.message, data), 400

    def pull_message(self, queue_id):
        message = self.queue_service.pull_message(queue_id)
        if not message:
            return generate_response(False, "Queue not found"), 404
        return generate_response(True, "Message pulled", message.to_dict()), 200




import grpc
from google.protobuf.json_format import MessageToDict
from concurrent import futures
from src.utils import mom_pb2, mom_pb2_grpc
from src.services.queue_service import QueueService


class QueueServiceServicer(mom_pb2_grpc.QueueServiceServicer):
    def __init__(self):
        self.service = QueueService()

    def CreateQueue(self, request, context):
        data_dict = MessageToDict(request)
        self.service.create_queue({"queue_id": data_dict["queueId"]}, data_dict["user"])
        return mom_pb2.Response(success=True, message="Queue created")

    def ListQueues(self, request, context):
        queues = self.service.get_queues()
        return mom_pb2.ListQueuesResponse(queues=queues)

    def PushMessage(self, request, context):
        try:
            success = self.service.push_message({
                "content": request.content,
                "sender": request.sender
            }, request.queue_id)
            message = "Message pushed" if success else "Queue not found"
            return mom_pb2.Response(success=success, message=message)
        except Exception as e:
            print(f"Failed to push message: {e}")
            return mom_pb2.Response(success=False, message=str(e))

    def PullMessage(self, request, context):
        message = self.service.pull_message(request.queue_id)
        if message:
            return mom_pb2.MessageResponse(message=mom_pb2.Message(
                message_id=message.message_id,
                parent=message.parent,
                content=message.content,
                sender=message.sender,
                timestamp=message.timestamp
            ))
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Queue not found")
        return mom_pb2.MessageResponse()

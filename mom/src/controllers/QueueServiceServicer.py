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
            return mom_pb2.MessageResponse(
                success=True,
                message="Message retrieved",
                data=mom_pb2.Message(
                    message_id=message.message_id,
                    parent=message.parent,
                    content=message.content,
                    sender=message.sender,
                    timestamp=message.timestamp
                )
            )
        return mom_pb2.MessageResponse(success=False, message="There are no messages in the queue")

    def DeleteQueue(self, request, context):
        success = self.service.delete_queue(request.queue_id, request.user)
        message = "Queue deleted" if success else "Queue not found or uathorization failed"
        return mom_pb2.Response(success=success, message=message)

    def GetQueue(self, request, context):
        try:
            queue_data = self.service.export_queue(request.target)
            return mom_pb2.GetQueueResponse(
                success=True,
                message="Queue exported",
                data=queue_data
            )
        except Exception as e:
            print(f"Failed to export queue: {e}")
            return mom_pb2.GetQueueResponse(success=False, message=str(e))

    def ImportQueue(self, request, context):
        try:
            self.service.import_queue(request.queue)
            return mom_pb2.Response(success=True, message="Queue imported")
        except Exception as e:
            print(f"Failed to import queue: {e}")
            return mom_pb2.Response(success=False, message=str(e))

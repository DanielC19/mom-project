import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grpc
from concurrent import futures
import mom_pb2, mom_pb2_grpc
from services.topics_services import TopicsService
from services.queue_service import QueueService

class TopicServiceServicer(mom_pb2_grpc.TopicServiceServicer):
    def __init__(self):
        self.service = TopicsService()

    def CreateTopic(self, request, context):
        success = self.service.create_topic(request.topic_id)
        message = "Topic created" if success else "Topic already exists"
        return mom_pb2.Response(success=success, message=message)

    def PublishMessage(self, request, context):
        success = self.service.publish_message(request.topic_id, {
            "content": request.content,
            "sender": request.sender
        })
        message = "Message published" if success else "Topic not found"
        return mom_pb2.Response(success=success, message=message)

    def Subscribe(self, request, context):
        success = self.service.subscribe(request.topic_id, request.subscriber_id)
        message = "Subscribed successfully" if success else "Subscription failed"
        return mom_pb2.Response(success=success, message=message)

    def Unsubscribe(self, request, context):
        success = self.service.unsubscribe(request.topic_id, request.subscriber_id)
        message = "Unsubscribed successfully" if success else "Unsubscription failed"
        return mom_pb2.Response(success=success, message=message)

    def ListTopics(self, request, context):
        topics = self.service.get_topics()
        return mom_pb2.ListTopicsResponse(topics=topics)

    def PullMessages(self, request, context):
        messages = self.service.pull_messages(request.topic_id, request.subscriber_id)
        return mom_pb2.MessagesResponse(messages=[
            mom_pb2.Message(
                message_id=msg.message_id,
                parent=msg.parent,
                content=msg.content,
                sender=msg.sender,
                timestamp=msg.timestamp
            ) for msg in messages
        ])

class QueueServiceServicer(mom_pb2_grpc.QueueServiceServicer):
    def __init__(self):
        self.service = QueueService()

    def CreateQueue(self, request, context):
        self.service.create_queue({"queue_id": request.queue_id})
        return mom_pb2.Response(success=True, message="Queue created")

    def ListQueues(self, request, context):
        queues = self.service.get_queues()
        return mom_pb2.ListQueuesResponse(queues=queues)

    def PushMessage(self, request, context):
        success = self.service.push_message({
            "content": request.content,
            "sender": request.sender
        }, request.queue_id)
        message = "Message pushed" if success else "Queue not found"
        return mom_pb2.Response(success=success, message=message)

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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mom_pb2_grpc.add_TopicServiceServicer_to_server(TopicServiceServicer(), server)
    mom_pb2_grpc.add_QueueServiceServicer_to_server(QueueServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

import grpc
from google.protobuf.json_format import MessageToDict
from concurrent import futures
from src.utils import mom_pb2, mom_pb2_grpc
from src.services.topics_services import TopicsService

class TopicServiceServicer(mom_pb2_grpc.TopicServiceServicer):
    def __init__(self):
        self.service = TopicsService()

    def CreateTopic(self, request, context):
        data_dict = MessageToDict(request)
        success = self.service.create_topic(data_dict["topicId"], data_dict["user"])
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
        print(f"Topics: {topics}")

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

    def DeleteTopic(self, request, context):
        #TODO: review that only the creator be capablke to delete
        success = self.service.delete_topic(request.topic_id)
        message = "Topic deleted" if success else "Topic not found"
        return mom_pb2.Response(success=success, message=message)
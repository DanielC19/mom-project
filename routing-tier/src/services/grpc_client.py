import grpc
from src.grpc_client import mom_pb2, mom_pb2_grpc  # Correct the import path

class GRPCClient:
    def __init__(self, host="localhost", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.topic_stub = mom_pb2_grpc.TopicServiceStub(self.channel)
        self.queue_stub = mom_pb2_grpc.QueueServiceStub(self.channel)

    def create_queue(self, queue_id):
        request = mom_pb2.CreateQueueRequest(queue_id=queue_id)
        return self.queue_stub.CreateQueue(request)

    def list_queues(self):
        request = mom_pb2.Empty()
        return self.queue_stub.ListQueues(request)

    def push_message(self, queue_id, content, sender):
        request = mom_pb2.PushMessageRequest(queue_id=queue_id, content=content, sender=sender)
        return self.queue_stub.PushMessage(request)

    def pull_message(self, queue_id):
        request = mom_pb2.PullMessageRequest(queue_id=queue_id)
        return self.queue_stub.PullMessage(request)

    def create_topic(self, topic_id):
        request = mom_pb2.CreateTopicRequest(topic_id=topic_id)
        return self.topic_stub.CreateTopic(request)

    def publish_message(self, topic_id, content, sender):
        request = mom_pb2.PublishMessageRequest(topic_id=topic_id, content=content, sender=sender)
        return self.topic_stub.PublishMessage(request)

    def subscribe(self, topic_id, subscriber_id):
        request = mom_pb2.SubscribeRequest(topic_id=topic_id, subscriber_id=subscriber_id)
        return self.topic_stub.Subscribe(request)

    def unsubscribe(self, topic_id, subscriber_id):
        request = mom_pb2.UnsubscribeRequest(topic_id=topic_id, subscriber_id=subscriber_id)
        return self.topic_stub.Unsubscribe(request)

    def delete_topic(self, topic_id):
        request = mom_pb2.DeleteTopicRequest(topic_id=topic_id)
        return self.topic_stub.DeleteTopic(request)

    def subscribe(self, topic_id, subscriber_id):
        request = mom_pb2.SubscribeRequest(topic_id=topic_id, subscriber_id=subscriber_id)
        return self.topic_stub.Subscribe(request)

    def pull_messages(self, topic_id, subscriber_id):
        request = mom_pb2.PullMessagesRequest(topic_id=topic_id, subscriber_id=subscriber_id)
        return self.topic_stub.PullMessages(request)

    def list_topics(self):
        request = mom_pb2.Empty()
        return self.topic_stub.ListTopics(request)

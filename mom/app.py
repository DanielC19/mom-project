import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grpc
from concurrent import futures
from src.utils import mom_pb2, mom_pb2_grpc
from src.services.topics_services import TopicsService
from src.services.queue_service import QueueService
from google.protobuf.json_format import MessageToDict

from kazoo.client import KazooClient
import socket
import os
import random

ZOOKEEPER_HOSTS = "127.0.0.1:2181"
HOSTS_PATH = "/hosts_service"

class TopicServiceServicer(mom_pb2_grpc.TopicServiceServicer):
    def __init__(self):
        self.service = TopicsService()

    def CreateTopic(self, request, context):

        data_dict = MessageToDict(request)
        print(data_dict)
        success = self.service.create_topic(data_dict["topic_id"])
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
        data_dict = MessageToDict(request)
        self.service.create_queue({"queue_id": data_dict["queueId"]})
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


def register_with_zookeeper(zk, port):
    zk.ensure_path(HOSTS_PATH)
    hostname = socket.gethostbyname(socket.gethostname())
    address = f"{hostname}:{port}"
    instance_name = f"{hostname}_{port}"
    node_path = f"{HOSTS_PATH}/{instance_name}"
    if not zk.exists(node_path):
        zk.create(node_path, ephemeral=True, value=address.encode())
    print(f"Registered MOM instance: {node_path} -> {address}")

def update_hosts(self, children):
    """Update the list of available MOM hosts."""
    self.hosts = []
    for child in children:
        data, _ = self.zk.get(f"{HOSTS_PATH}/{child}")
        self.hosts.append(data.decode())
    print(f"Updated MOM hosts: {self.hosts}")

def get_mom_host(self):
    """Select a MOM host using round-robin or random selection."""
    if not self.hosts:
        raise Exception("No MOM hosts available")
    return random.choice(self.hosts)  # Selección aleatoria


if __name__ == "__main__":
    zk = KazooClient(hosts=ZOOKEEPER_HOSTS)
    zk.start()

    port = 5001
    # Register the MOM instance with Zookeeper
    register_with_zookeeper(zk, port)

    serve()

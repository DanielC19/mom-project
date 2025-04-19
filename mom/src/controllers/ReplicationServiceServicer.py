from src.utils.replication_pb2 import GetTopicResponse, GetQueueResponse, FailOverResponse, Topic as ProtoTopic, Queue as ProtoQueue, Message as ProtoMessage
from src.utils.replication_pb2_grpc import ReplicationServiceServicer as BaseReplicationServiceServicer
from src.services.topics_services import TopicsService
from src.services.queue_service import QueueService
import grpc
from src.utils.replication_pb2 import GetTopicRequest, GetQueueRequest
from src.utils.replication_pb2_grpc import ReplicationServiceStub

class ReplicationServiceServicer(BaseReplicationServiceServicer):
    def __init__(self):
        self.topics_service = TopicsService()
        self.queue_service = QueueService()

    def GetTopic(self, request, context):
        # Buscar el topic en la lista de topics
        topics = self.topics_service.get_topics()
        topic_data = next((t for t in topics if t["topic_id"] == request.topic_id), None)
        if topic_data:
            messages = self.topics_service.get_topic_messages(request.topic_id)  # nueva obtención de mensajes
            proto_topic = ProtoTopic(topic_id=topic_data["topic_id"], autor=topic_data["autor"], messages=messages)
            return GetTopicResponse(success=True, message="Topic found", topic=proto_topic)
        return GetTopicResponse(success=False, message="Topic not found", messages=[])

    def GetQueue(self, request, context):
        queues = self.queue_service.get_queues()
        queue_data = next((q for q in queues if q["queue_id"] == request.queue_id), None)
        if queue_data:
            messages = self.queue_service.get_queue_messages(request.queue_id)  # nueva obtención de mensajes
            proto_queue = ProtoQueue(queue_id=queue_data["queue_id"], autor=queue_data["autor"], messages=messages)
            return GetQueueResponse(success=True, message="Queue found", queue=proto_queue)
        return GetQueueResponse(success=False, message="Queue not found", messages=[])

    def FailOver(self, request, context):
        if request.isTopic:
            with grpc.insecure_channel(f"{request.target}:50051") as channel:
                stub = ReplicationServiceStub(channel)
                topic_request = GetTopicRequest(topic_id=request.id)
                topic_response = stub.GetTopic(topic_request)
            return FailOverResponse(success=topic_response.success, message=f"Topic failover: {topic_response.message}")
        else:
            with grpc.insecure_channel(f"{request.target}:50051") as channel:
                stub = ReplicationServiceStub(channel)
                queue_request = GetQueueRequest(queue_id=request.id)
                queue_response = stub.GetQueue(queue_request)
            return FailOverResponse(success=queue_response.success, message=f"Queue failover: {queue_response.message}")


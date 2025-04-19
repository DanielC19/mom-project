
# Nueva clase que implementa la funcionalidad de enviar solicitudes (lado cliente)
class ReplicationServiceClient:
    def __init__(self, host="localhost", port=50051):
        import grpc
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        from src.utils.replication_pb2_grpc import ReplicationServiceStub
        self.stub = ReplicationServiceStub(self.channel)

    def get_topic(self, topic_id):
        from src.utils.replication_pb2 import GetTopicRequest
        request = GetTopicRequest(topic_id=topic_id)
        return self.stub.GetTopic(request)

    def get_queue(self, queue_id):
        from src.utils.replication_pb2 import GetQueueRequest
        request = GetQueueRequest(queue_id=queue_id)
        return self.stub.GetQueue(request)

 
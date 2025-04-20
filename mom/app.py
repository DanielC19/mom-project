import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grpc
from concurrent import futures
from src.utils import mom_pb2_grpc
from kazoo.client import KazooClient
import socket
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.controllers.TopicServiceServicer import TopicServiceServicer
from src.controllers.QueueServiceServicer import QueueServiceServicer

ZOOKEEPER_HOSTS = "127.0.0.1:2181" 
HOSTS_PATH = "/hosts_service"

class RestartHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected change in {event.src_path}. Restarting application...")
            os.execv(sys.executable, ['python'] + sys.argv)

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mom_pb2_grpc.add_TopicServiceServicer_to_server(TopicServiceServicer(), server)
    mom_pb2_grpc.add_QueueServiceServicer_to_server(QueueServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.add_insecure_port(f"[::]:{port}")
    print(f"gRPC server running on port 50051 and {port}")
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

    # Set up watchdog observer
    path_to_watch = os.path.dirname(os.path.abspath(__file__))
    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        serve(port)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

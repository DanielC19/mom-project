from flask import Flask
from flask_cors import CORS
from kazoo.client import KazooClient
import socket
from src.routes.queue_routes import queue_bp
from src.routes.topics_routes import topic_bp
import os
import random

ZOOKEEPER_HOSTS = "127.0.0.1:2181"
HOSTS_PATH = "/hosts_service"

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(queue_bp)
    app.register_blueprint(topic_bp)

    return app

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

class GRPCClient:
    def __init__(self, host, port):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.topic_stub = mom_pb2_grpc.TopicServiceStub(self.channel)
        self.queue_stub = mom_pb2_grpc.QueueServiceStub(self.channel)

if __name__ == "__main__":
    # Initialize Kazoo client
    zk = KazooClient(hosts=ZOOKEEPER_HOSTS)
    zk.start()

    port = 5001
    # Register the MOM instance with Zookeeper
    register_with_zookeeper(zk, port)

    # Start the Flask app
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)
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
    # Ensure the service path exists
    zk.ensure_path(HOSTS_PATH)

    # Get the hostname or IP address of the current machine
    hostname = socket.gethostbyname(socket.gethostname())
    address = f"{hostname}:{port}"

    # Register this MOM instance with a unique node in Zookeeper
    instance_name = f"{hostname}_{port}"
    node_path = f"{HOSTS_PATH}/{instance_name}"

    # Check if the node already exists
    if zk.exists(node_path):
        print(f"Node {node_path} already exists. Skipping...")
        return

    # Create the node as ephemeral
    zk.create(node_path, ephemeral=True)
    print(f"Registered MOM instance: {node_path} -> {address}")

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
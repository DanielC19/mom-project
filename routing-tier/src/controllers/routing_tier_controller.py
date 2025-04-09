from kazoo.client import KazooClient
from src.services.grpc_client import GRPCClient
import random
import time
import requests
from google.protobuf.json_format import MessageToDict

ZOOKEEPER_HOSTS = "127.0.0.1:2181"
HOSTS_PATH = "/hosts_service"
QUEUE_PATH = "/queue_service"

class RoutingTier:
    def __init__(self):
        self.grpc_client = GRPCClient()  # Initialize gRPC client
        self.zk = KazooClient(hosts=ZOOKEEPER_HOSTS)
        self.zk.start()
        self.queues = {}  # Store queue metadata (leader, follower)
        self.hosts = []  # List of available hosts

        # Ensure the service path exists
        self.zk.ensure_path(HOSTS_PATH)
        self.zk.ensure_path(QUEUE_PATH)

        existing_queues = self.zk.get_children(QUEUE_PATH)
        for queue_name in existing_queues:
            data, _ = self.zk.get(f"{QUEUE_PATH}/{queue_name}")
            leader, follower = data.decode().split("|")
            self.queues[queue_name] = {"leader": leader, "follower": follower}
            print(f"Loaded existing queues: {self.queues}")


        # Watch for changes in hosts
        @self.zk.ChildrenWatch(HOSTS_PATH)
        def watch_hosts(children):
            self.update_hosts(children)

        @self.zk.ChildrenWatch(QUEUE_PATH)
        def watch_hosts(children):
            print(f"Queues Zoo: {children}")

    def update_hosts(self, children):
        """Update the list of available hosts."""
        self.hosts = children
        print(f"Updated hosts: {self.hosts}")

    def get_queues(self):
        """Get the list of queues."""
        try:
            response = self.grpc_client.list_queues()
            data_dict = MessageToDict(response)
            print(data_dict)
            return {"data": data_dict["queues"], "success": True }
        except Exception as e:
            print(f"Failed to create queue via gRPC: {e}")
            return {"success": False, "message": str(e)}
    def create_queue(self, queue_name, endpoint, data):
        """Create a new queue using gRPC."""
        try:
            response = self.grpc_client.create_queue(queue_name)
            print(f"Queue created via gRPC: {response.message}")
            return {"success": response.success, "message": response.message}
        except Exception as e:
            print(f"Failed to create queue via gRPC: {e}")
            return {"success": False, "message": str(e)}

    def handle_failover(self, queue_name):
        """Handle failover for a queue when the leader or follower goes down."""
        if queue_name not in self.queues:
            print(f"Queue {queue_name} does not exist.")
            return

        queue_info = self.queues[queue_name]
        leader = queue_info["leader"]
        follower = queue_info["follower"]

        if leader not in self.hosts:
            print(f"Leader {leader} for queue {queue_name} is down. Promoting follower.")
            self.queues[queue_name]["leader"] = follower

            new_follower_candidates = [host for host in self.hosts if host != follower]
            if new_follower_candidates:
                new_follower = random.choice(new_follower_candidates)
                self.queues[queue_name]["follower"] = new_follower
                self.zk.set(f"{QUEUE_PATH}/{queue_name}", f"{follower}|{new_follower}".encode())
                print(f"New leader for queue {queue_name} is {follower}. New follower is {new_follower}.")
            else:
                print(f"No available hosts to assign as a new follower for queue {queue_name}.")
                self.queues[queue_name]["follower"] = None

        elif follower not in self.hosts:
            print(f"Follower {follower} for queue {queue_name} is down. Assigning a new follower.")
            new_follower_candidates = [host for host in self.hosts if host != leader]
            if new_follower_candidates:
                new_follower = random.choice(new_follower_candidates)
                self.queues[queue_name]["follower"] = new_follower
                self.zk.set(f"{QUEUE_PATH}/{queue_name}", f"{leader}|{new_follower}".encode())
                print(f"New follower for queue {queue_name} is {new_follower}.")
            else:
                print(f"No available hosts to assign as a new follower for queue {queue_name}.")
                self.queues[queue_name]["follower"] = None

    def monitor_queues(self):
        """Monitor queues and handle failovers."""
        while True:
            for queue_name in list(self.queues.keys()):
                self.handle_failover(queue_name)
            time.sleep(5)

    def route_request(self, queue_name, endpoint, method="GET", data=None):
        """Route a request to the MOM using gRPC."""
        try:
            host = self.get_mom_host()
            host_ip, host_port = host.split(":")
            grpc_client = GRPCClient(host_ip, int(host_port))

            if method == "PUT":
                response = grpc_client.push_message(queue_name, data["content"], data["sender"])
            elif method == "GET":
                response = grpc_client.pull_message(queue_name)
            else:
                raise ValueError("Unsupported method")

            return {"success": response.success, "message": response.message, "data": response.data}
        except Exception as e:
            print(f"Failed to route request via gRPC: {e}")
            return {"success": False, "message": str(e)}




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
        self.grpc_client = GRPCClient()  # Initialize gRPC client ONLY FOR BROADCAST
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

    def queue_grpc_client(self, queue_id):
        """Create a gRPC client for the specified queue.
        Returns the leader and follower (optional) clients."""

        leader, follower = self.queues[queue_id]["leader"], self.queues[queue_id]["follower"]
        leader_ip, leader_port = leader.split("_")
        leader_client = GRPCClient(host=leader_ip, port=int(leader_port))

        if follower:
            follower_ip, follower_port = follower.split("_")
            follower_client = GRPCClient(host=follower_ip, port=int(follower_port))
            return leader_client, follower_client

        return leader_client, None

    def get_queues(self):
        """Get the list of queues."""
        return list(self.queues.keys())

    def get_topics(self):
        """Get the list of queues."""
        return list(self.queues.keys())

    def create_queue(self, queue_name, user):
        """Create a new queue and assign a leader and follower."""
        if queue_name in self.queues:
            print(f"Queue {queue_name} already exists.")
            return {"success": False, "message": "Queue already exists."}

        leader = random.choice(self.hosts)
        if len(self.hosts) >= 2:
            follower = random.choice([host for host in self.hosts if host != leader])
        else:
            follower = None

        self.queues[queue_name] = {"leader": leader, "follower": follower}

        try:
            self.zk.create(f"{QUEUE_PATH}/{queue_name}", f"{leader}|{follower}".encode())
            print(f"Created queue {queue_name} with leader {leader} and follower {follower}.")
        except Exception as e:
            print(f"Failed to create Zookeeper node for queue {queue_name}: {str(e)}")
            return {"success": False, "message": f"Zookeeper error: {str(e)}"}

        try:
            leader_client, follower_client = self.queue_grpc_client(queue_name)
            leader_response = leader_client.create_queue(queue_name, user)

            if follower_client:
                try:
                    follower_client.create_queue(queue_name, user)
                except Exception as e:
                    print(f"Failed to create queue on follower {follower}: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to create queue via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def create_topic(self, topic_name, user):
        """Create a new topic and assign a leader and follower."""
        if topic_name in self.queues:
            print(f"Topic {topic_name} already exists.")
            return {"success": False, "message": "Topic already exists."}

        leader = random.choice(self.hosts)
        if len(self.hosts) >= 2:
            follower = random.choice([host for host in self.hosts if host != leader])
        else:
            follower = None

        self.queues[topic_name] = {"leader": leader, "follower": follower}
        self.zk.create(f"{QUEUE_PATH}/{topic_name}", f"{leader}|{follower}".encode())
        print(f"Created topic {topic_name} with leader {leader} and follower {follower}.")

        try:
            leader_client, follower_client = self.queue_grpc_client(topic_name)
            leader_response = leader_client.create_topic(topic_name, user)

            if follower_client:
                try:
                    follower_client.create_topic(topic_name, user)
                except Exception as e:
                    print(f"Failed to create topic on follower {follower}: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to create topic via gRPC: {str(e)}")
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

    def push_message_queue(self, queue_id, data, user):
        """Push a message to the queue using gRPC."""
        try:
            leader_client, follower_client = self.queue_grpc_client(queue_id)
            leader_response = leader_client.push_message(queue_id, data["content"], user)

            if follower_client:
                try:
                    follower_client.push_message(queue_id, data["content"], user)
                except Exception as e:
                    print(f"Failed to push message to follower for {queue_id}: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to push message via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def pull_message_queue(self, queue_id):
        """Pull a message from the queue using gRPC."""
        try:
            leader_client, follower_client = self.queue_grpc_client(queue_id)
            leader_response = leader_client.pull_message(queue_id)

            if follower_client:
                try:
                    follower_client.pull_message(queue_id)
                except Exception as e:
                    print(f"Failed to pull message from follower for {queue_id}: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to pull message via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def push_message_topic(self, topic_name, data, user):
        """Push a message to a topic using gRPC."""
        try:
            leader_client, follower_client = self.queue_grpc_client(topic_name)
            leader_response = leader_client.push_message(topic_name, data["content"], user)
            if follower_client:
                try:
                    follower_client.push_message(topic_name, data["content"], user)
                except Exception as e:
                    print(f"Failed to push message to follower for {topic_name}: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to push message to topic via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def pull_message_topic(self, topic_name, user_id):
        """Pull a message from a topic using gRPC."""
        try:
            leader_client, follower_client = self.queue_grpc_client(topic_name)
            leader_response = leader_client.pull_message(topic_name, user_id)
            if follower_client:
                try:
                    follower_client.pull_message(topic_name, user_id)
                except Exception as e:
                    print(f"Failed to pull message from follower for {topic_name}: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to pull message from topic via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def subscribe_topic(self, topic_id, subscriber_id):
        try:
            leader_client, follower_client = self.queue_grpc_client(topic_id)
            leader_response = leader_client.subscribe(topic_id, subscriber_id)
            if follower_client:
                try:
                    follower_client.subscribe(topic_id, subscriber_id)
                except Exception as e:
                    print(f"Failed to subscribe to topic on follower {topic_id}: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to subscribe to topic via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def unsubscribe_topic(self, topic_id, subscriber_id):
        try:
            leader_client, follower_client = self.queue_grpc_client(topic_id)
            leader_response = leader_client.unsubscribe(topic_id, subscriber_id)
            if follower_client:
                try:
                    follower_client.unsubscribe(topic_id, subscriber_id)
                except Exception as e:
                    print(f"Failed to unsubscribe from topic on follower {topic_id}: {str(e)}")
            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to unsubscribe from topic via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def delete_topic(self, topic_id, user):
        try:
            leader_client, follower_client = self.queue_grpc_client(topic_id)
            leader_response = leader_client.delete_topic(topic_id, user)
            if follower_client:
                try:
                    follower_client.delete_topic(topic_id, user)
                except Exception as e:
                    print(f"Failed to delete topic on follower {topic_id}: {str(e)}")
            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to delete topic via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

import sys
from kazoo.client import KazooClient
from src.services.grpc_client import GRPCClient
import random
import time
from google.protobuf.json_format import MessageToDict

if len(sys.argv) > 1:
    ZOOKEEPER_HOSTS = sys.argv[1]
else:
    ZOOKEEPER_HOSTS = "127.0.0.1:2181"

HOSTS_PATH = "/hosts_service"
QUEUE_PATH = "/queue_service"
TOPIC_PATH = "/topic_service"

class RoutingTier:
    def __init__(self):
        self.grpc_client = GRPCClient()  # Initialize gRPC client ONLY FOR BROADCAST
        self.zk = KazooClient(hosts=ZOOKEEPER_HOSTS)
        max_retries = 5
        attempt = 0
        while attempt < max_retries:
            try:
                self.zk.start()
                break
            except Exception as e:
                attempt += 1
                print(f"Attempt {attempt} to connect to Zookeeper failed: {e}")
                time.sleep(3)
        if attempt == max_retries:
            print("Error connecting to Zookeeper after maximum retries")
            self.zk = None
        self.queues = {}
        self.topics = {}
        self.hosts = []  # List of available hosts

        # Ensure the service path exists
        self.zk.ensure_path(HOSTS_PATH)
        self.zk.ensure_path(QUEUE_PATH)
        self.zk.ensure_path(TOPIC_PATH)

        self.update_hosts(self.zk.get_children(HOSTS_PATH))

        queues = []
        topics = []
        for host in self.hosts:
            host_ip, host_port = host.split("_")
            host_client = GRPCClient(host=host_ip, port=int(host_port))
            queues.append(host_client.list_queues())
            topics.append(host_client.list_topics())
        print(f"Hosts Queues: {queues}")

        existing_queues = self.zk.get_children(QUEUE_PATH)
        for queue_name in existing_queues:
            if queue_name not in self.queues:
                self.zk.delete(f"{QUEUE_PATH}/{queue_name}")
                continue
            data, _ = self.zk.get(f"{QUEUE_PATH}/{queue_name}")
            leader, follower, autor = data.decode().split("|")
            self.queues[queue_name] = {"leader": leader, "follower": follower, "autor": autor}
            print(f"Loaded existing queues: {self.queues}")

        existing_topics = self.zk.get_children(TOPIC_PATH)
        for topic_name in existing_topics:
            if topic_name not in self.topics:
                self.zk.delete(f"{TOPIC_PATH}/{topic_name}")
                continue
            data, _ = self.zk.get(f"{TOPIC_PATH}/{topic_name}")
            leader, follower, autor = data.decode().split("|")
            self.queues[topic_name] = {"leader": leader, "follower": follower, "autor": autor}
            print(f"Loaded existing queues: {self.topics}")


        # Watch for changes in hosts
        @self.zk.ChildrenWatch(HOSTS_PATH)
        def watch_hosts(children):
            self.update_hosts(children)

        @self.zk.ChildrenWatch(QUEUE_PATH)
        def watch_hosts(children):
            print(f"Queues Zoo: {children}")

        @self.zk.ChildrenWatch(TOPIC_PATH)
        def watch_hosts(children):
            print(f"TOPICS Zoo: {children}")

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

        if follower and follower != "None":
            follower_ip, follower_port = follower.split("_")
            follower_client = GRPCClient(host=follower_ip, port=int(follower_port))
            return leader_client, follower_client

        return leader_client, None

    def topic_grpc_client(self, topic_id):
        """Create a gRPC client for the specified queue.
        Returns the leader and follower (optional) clients."""

        leader, follower = self.topics[topic_id]["leader"], self.topics[topic_id]["follower"]
        leader_ip, leader_port = leader.split("_")
        leader_client = GRPCClient(host=leader_ip, port=int(leader_port))

        if follower and follower != "None":
            follower_ip, follower_port = follower.split("_")
            follower_client = GRPCClient(host=follower_ip, port=int(follower_port))
            return leader_client, follower_client

        return leader_client, None

    def get_queues(self):
        """Get the list of queues."""
        queue_list = list(self.queues.keys())
        response= []
     
        for queue in queue_list:
            response.append({"queue_id": queue, "autor": self.queues[queue]["autor"]})
        return response

    def get_topics(self):
        """Get the list of queues."""
        topic_list = list(self.topics.keys())
        response= []
     
        for topic in topic_list:
            response.append({"topic_id": topic, "autor": self.topics[topic]["autor"]})
    
        return response

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

        self.queues[queue_name] = {"leader": leader, "follower": follower, "autor": user}

        try:
            autor= user
            self.zk.create(f"{QUEUE_PATH}/{queue_name}", f"{leader}|{follower}|{autor}".encode())
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
        if topic_name in self.topics:
            print(f"Topic {topic_name} already exists.")
            return {"success": False, "message": "Topic already exists."}

        leader = random.choice(self.hosts)
        if len(self.hosts) >= 2:
            follower = random.choice([host for host in self.hosts if host != leader])
        else:
            follower = None

        self.topics[topic_name] = {"leader": leader, "follower": follower, "autor": user}
        autor= user
        self.zk.create(f"{TOPIC_PATH}/{topic_name}", f"{leader}|{follower}|{autor}".encode())
        print(f"Created topic {topic_name} with leader {leader} and follower {follower}.")

        try:
            leader_client, follower_client = self.topic_grpc_client(topic_name)
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

    def handle_failover_queue(self, queue_name, retry=False):
        if queue_name not in self.queues:
            print(f"Queue {queue_name} does not exist.")
            return

        q_info = self.queues[queue_name]
        leader = q_info["leader"]
        follower = q_info["follower"]

        if leader == "None" and follower == "None":
            print(f"Queue {queue_name} has no leader or follower. Deleting queue.")
            self.zk.delete(f"{QUEUE_PATH}/{queue_name}")
            del self.queues[queue_name]
            return

        if leader not in self.hosts:
            print(f"Leader {leader} for queue {queue_name} is down. Promoting follower.")
            self.queues[queue_name]["leader"] = follower
            new_follower_candidates = [host for host in self.hosts if host != follower]
            if new_follower_candidates:
                new_follower = random.choice(new_follower_candidates)
                new_follower_ip, new_follower_port = new_follower.split("_")
                new_follower_client = GRPCClient(host=new_follower_ip, port=int(new_follower_port))

                _, follower_client = self.queue_grpc_client(queue_name)
                exported_topic = follower_client.export_queue(queue_name)
                new_follower_client.import_queue(exported_topic.data)

                self.queues[queue_name]["follower"] = new_follower
                self.zk.set(f"{QUEUE_PATH}/{queue_name}", f"{follower}|{new_follower}".encode())
                print(f"New leader for queue {queue_name} is {follower}.")
            else:
                self.queues[queue_name]["follower"] = None
                self.zk.set(f"{QUEUE_PATH}/{queue_name}", f"{follower}|None".encode())

        elif follower not in self.hosts:
            print(f"Follower {follower} for queue {queue_name} is down. Assigning a new follower.")
            new_follower_candidates = [host for host in self.hosts if host != leader]
            if new_follower_candidates:
                new_follower = random.choice(new_follower_candidates)
                new_follower_ip, new_follower_port = new_follower.split("_")
                new_follower_client = GRPCClient(host=new_follower_ip, port=int(new_follower_port))

                leader_client, _ = self.queue_grpc_client(queue_name)
                exported_topic = leader_client.export_queue(queue_name)
                new_follower_client.import_queue(exported_topic.data)

                self.queues[queue_name]["follower"] = new_follower
                self.zk.set(f"{QUEUE_PATH}/{queue_name}", f"{leader}|{new_follower}".encode())
                print(f"New follower for queue {queue_name} is {new_follower}.")
            else:
                self.queues[queue_name]["follower"] = None
                self.zk.set(f"{QUEUE_PATH}/{queue_name}", f"{leader}|None".encode())

    def handle_failover_topic(self, topic_name):
        if topic_name not in self.topics:
            print(f"Topic {topic_name} does not exist.")
            return

        t_info = self.topics[topic_name]
        leader = t_info["leader"]
        follower = t_info["follower"]

        if (leader == "None" or not leader) and (follower == "None" or not follower):
            print(f"Topic {topic_name} has no leader or follower. Deleting topic.")
            self.zk.delete(f"{TOPIC_PATH}/{topic_name}")
            del self.topics[topic_name]
            return

        if leader not in self.hosts:
            print(f"Leader {leader} for topic {topic_name} is down. Promoting follower.")
            self.topics[topic_name]["leader"] = follower
            new_follower_candidates = [host for host in self.hosts if host != follower]
            if new_follower_candidates:
                new_follower = random.choice(new_follower_candidates)
                new_follower_ip, new_follower_port = new_follower.split("_")
                new_follower_client = GRPCClient(host=new_follower_ip, port=int(new_follower_port))

                leader_client, _ = self.topic_grpc_client(topic_name)
                exported_topic = leader_client.export_topic(topic_name)
                new_follower_client.import_topic(exported_topic.data)

                self.topics[topic_name]["follower"] = new_follower
                self.zk.set(f"{TOPIC_PATH}/{topic_name}", f"{leader}|{new_follower}".encode())
                print(f"New leader for topic {topic_name} is {leader}.")
            else:
                self.topics[topic_name]["follower"] = None
                self.zk.set(f"{TOPIC_PATH}/{topic_name}", f"{leader}|None".encode())

        elif follower not in self.hosts:
            print(f"Follower {follower} for topic {topic_name} is down. Assigning a new follower.")
            new_follower_candidates = [host for host in self.hosts if host != leader]
            if new_follower_candidates:
                new_follower = random.choice(new_follower_candidates)
                new_follower_ip, new_follower_port = new_follower.split("_")
                new_follower_client = GRPCClient(host=new_follower_ip, port=int(new_follower_port))

                leader_client, _ = self.topic_grpc_client(topic_name)
                exported_topic = leader_client.export_topic(topic_name)
                new_follower_client.import_topic(exported_topic.data)

                self.topics[topic_name]["follower"] = new_follower
                self.zk.set(f"{TOPIC_PATH}/{topic_name}", f"{leader}|{new_follower}".encode())
                print(f"New follower for topic {topic_name} is {new_follower}.")
            else:
                self.topics[topic_name]["follower"] = None
                self.zk.set(f"{TOPIC_PATH}/{topic_name}", f"{follower}|None".encode())

    def monitor_queues(self):
        """Monitor queues and handle failovers."""
        while True:
            for queue_name in list(self.queues.keys()):
                self.handle_failover_queue(queue_name)
            time.sleep(3)

    def monitor_topics(self):
        """Monitor queues and handle failovers."""
        while True:
            for topic in list(self.topics.keys()):
                self.handle_failover_topic(topic)
            time.sleep(3)

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

            if not leader_response.success and leader_response.message == "Queue is empty":
                        return {"success": False, "message": "Queue is empty"}

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
            leader_client, follower_client = self.topic_grpc_client(topic_name)
            leader_response = leader_client.publish_message(topic_name, data["content"], user)
            if follower_client:
                try:
                    print(follower_client)
                    follower_client.publish_message(topic_name, data["content"], user)
                except Exception as e:
                    print(f"Failed to push message to follower for {topic_name}: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to push message to topic via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def pull_message_topic(self, topic_name, user_id):
        """Pull a message from a topic using gRPC."""
        try:
            leader_client, follower_client = self.topic_grpc_client(topic_name)
            leader_response = leader_client.pull_messages(topic_name, user_id)
            if follower_client:
                try:
                    follower_client.pull_messages(topic_name, user_id)
                except Exception as e:
                    print(f"Failed to pull message from follower for {topic_name}: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to pull message from topic via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def subscribe_topic(self, topic_id, subscriber_id):
        try:
            leader_client, follower_client = self.topic_grpc_client(topic_id)
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
            leader_client, follower_client = self.topic_grpc_client(topic_id)
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
            leader_client, follower_client = self.topic_grpc_client(topic_id)
            leader_response = leader_client.delete_topic(topic_id, user)
            if follower_client:
                try:
                    follower_client.delete_topic(topic_id, user)
                except Exception as e:
                    print(f"Failed to delete topic on follower {topic_id}: {str(e)}")

            if leader_response.success:
                try:
                    self.zk.delete(f"{TOPIC_PATH}/{topic_id}")
                    del self.topics[topic_id]
                    print(f"Deleted topic {topic_id} from Zookeeper.")
                except Exception as e:
                    print(f"Failed to delete topic {topic_id} from Zookeeper: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to delete topic via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}

    def delete_queue(self, queue_id, user):
        try:
            print(f"Deleting queue {queue_id} by user {user}.")
            leader_client, follower_client = self.queue_grpc_client(queue_id)
            leader_response = leader_client.delete_queue(queue_id, user)
            if follower_client:
                try:
                    follower_client.delete_queue(queue_id, user)
                except Exception as e:
                    print(f"Failed to delete queue on follower {queue_id}: {str(e)}")

            if leader_response.success:
                try:
                    self.zk.delete(f"{QUEUE_PATH}/{queue_id}")
                    del self.queues[queue_id]
                    print(f"Deleted queue {queue_id} from Zookeeper.")
                except Exception as e:
                    print(f"Failed to delete queue {queue_id} from Zookeeper: {str(e)}")

            return MessageToDict(leader_response)
        except Exception as e:
            print(f"Failed to delete queue via gRPC: {str(e)}")
            return {"success": False, "message": str(e)}
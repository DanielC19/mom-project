from kazoo.client import KazooClient
import random
import time
import requests

ZOOKEEPER_HOSTS = "127.0.0.1:2181"
HOSTS_PATH = "/hosts_service"
QUEUE_PATH = "/queue_service"

class RoutingTier:
    def __init__(self):
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
        return list(self.queues.keys())

    def create_queue(self, queue_name, endpoint, data):
        """Create a new queue and assign a leader and follower."""
        if queue_name in self.queues:
            print(f"Queue {queue_name} already exists.")
            return

        leader = random.choice(self.hosts)
        if len(self.hosts) >= 2:
            follower = random.choice([host for host in self.hosts if host != leader])
        else:
            follower = None

        self.queues[queue_name] = {"leader": leader, "follower": follower}
        self.zk.create(f"{QUEUE_PATH}/{queue_name}", f"{leader}|{follower}".encode())
        print(f"Created queue {queue_name} with leader {leader} and follower {follower}.")

        self.route_request(queue_name, endpoint, method="POST", data=data)

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
        """Route a request to the leader of the queue, fallback to the follower if the leader fails."""
        if queue_name not in self.queues:
            print(f"Queue {queue_name} does not exist.")
            return {"error": "Queue does not exist"}, 404

        queue_info = self.queues[queue_name]
        leader = queue_info["leader"].replace("_", ":") if queue_info["leader"] else None
        follower = queue_info["follower"].replace("_", ":") if queue_info["follower"] else None

        # TODO: Replace with gRPC
        leader_url = f"http://{leader}/{endpoint}"
        follower_url = f"http://{follower}/{endpoint}"

        try:
            print(f"Routing request to leader: {leader_url}")
            response = requests.request(method, leader_url, json=data, timeout=5)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.RequestException as e:
            print(f"Leader {leader} failed. Error: {e}. Redirecting to follower: {follower_url}")
            try:
                response = requests.request(method, follower_url, json=data, timeout=5)
                response.raise_for_status()
                return response.json(), response.status_code
            except requests.RequestException as e:
                print(f"Follower {follower} also failed. Error: {e}.")
                return {"error": "Both leader and follower failed"}, 500




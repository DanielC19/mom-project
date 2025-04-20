import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.controllers.routing_tier_controller import RoutingTier

# Initialize the global RoutingTier instance
routing_tier = RoutingTier()

# Delete current queues
# routing_tier.zk.delete("/queue_service", recursive=True)

# Delete current hosts
# routing_tier.zk.delete("/hosts_service", recursive=True)

# Delete current topics
# routing_tier.zk.delete("/topic_service", recursive=True)
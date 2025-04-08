from src.controllers.routing_tier_controller import RoutingTier

# Initialize the global RoutingTier instance
routing_tier = RoutingTier()

# Delete current queues
# routing_tier.zk.delete("/queue_service", recursive=True)

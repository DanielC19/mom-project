from flask import Flask
from flask_cors import CORS
from src.routes.topics_routes import topic_bp
from src.routes.queue_routes import queue_bp
from src.services.routing_tier_service import routing_tier  # Import the global instance
import threading

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(topic_bp)
    app.register_blueprint(queue_bp)

    return app

def start_routing_tier():
    """Run the RoutingTier's listen method in a separate thread."""
    threading.Thread(target=routing_tier.monitor_queues, daemon=True).start()

if __name__ == "__main__":
    # Start the RoutingTier service
    start_routing_tier()

    # Start the Flask app
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

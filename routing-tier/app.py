from flask import Flask
from flask_cors import CORS
from src.routes.topics_routes import topic_bp
from src.routes.queue_routes import queue_bp
from src.routes.user_routes import user_bp  # Import the user routes
from src.services.routing_tier_service import routing_tier  # Import the global instance
from src.utils.database import db  
from models.user import User
import threading
import os
from flask_jwt_extended import JWTManager  # nueva importación

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(topic_bp)
    app.register_blueprint(queue_bp)
    app.register_blueprint(user_bp)  
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "your-secret-key"  # nueva configuración para JWT
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False  # elimina la expiración del token

    # Inicializar la base de datos con la app
    db.init_app(app)

    jwt = JWTManager(app)  # Inicialización de JWT

    return app

def start_routing_tier():
    """Run the RoutingTier's listen method in a separate thread."""
    threading.Thread(target=routing_tier.monitor_queues, daemon=True).start()
    threading.Thread(target=routing_tier.monitor_topics, daemon=True).start()

if __name__ == "__main__":
    start_routing_tier()

    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

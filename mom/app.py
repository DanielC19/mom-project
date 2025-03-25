from flask import Flask
from src.routes.queue_routes import queue_bp
from src.routes.topics_routes import topic_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(queue_bp)
    app.register_blueprint(topic_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
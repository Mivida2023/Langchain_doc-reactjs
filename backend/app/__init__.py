from flask import Flask
from flask_cors import CORS
from config.config import Config
from db.db import init_db


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    app.config.from_object(Config)

    # Validate environment variables
    Config.validate()

    # Initialize database
    init_db()

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.chat_routes import chat_bp
    from routes.model_routes import model_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chat_bp, url_prefix="/chats")
    app.register_blueprint(model_bp, url_prefix="/models")

    return app

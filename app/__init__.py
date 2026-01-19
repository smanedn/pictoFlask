import os
from flask import Flask

from .config import Config
from .extensions import db, socketio, login_manager
from .models import User
from .routes import register_blueprints


def create_app(config_class=Config) -> Flask:
    """Application factory."""
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )
    app.config.from_object(config_class)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    register_blueprints(app)

    # Import socket handlers to register them
    from . import sockets  # noqa: F401

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

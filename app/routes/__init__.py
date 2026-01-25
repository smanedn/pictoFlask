from flask import Flask

from .auth import auth_bp
from .main import main_bp
from .admin import admin_bp
from .messages import messages_bp


def register_blueprints(app: Flask) -> None:
    """Register all blueprints with the application."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(messages_bp)

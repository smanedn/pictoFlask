from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

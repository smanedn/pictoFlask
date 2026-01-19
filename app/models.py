from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
import secrets

from .extensions import db


# Default PictoFlask colors
PICTOFLASK_COLORS = [
    '#61829a', '#ba4900', '#fb0018', '#fb8afb',
    '#fb9200', '#f3e300', '#aafb00', '#00fb00',
    '#00a238', '#49db8a', '#30baf3', '#0059f3',
    '#000092', '#8a00d3', '#d300eb', '#fb0092'
]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.String(120), default='default.jpg')
    chat_color = db.Column(db.String(7), default='#61829a')  # Hex color for messages
    registered_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_username_change = db.Column(db.DateTime, nullable=True)
    message_count = db.Column(db.Integer, default=0)
    session_token = db.Column(db.String(64), nullable=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def can_change_username(self) -> bool:
        if self.last_username_change is None:
            return True
        delta = datetime.now(timezone.utc) - self.last_username_change
        return delta.days >= 30

    def refresh_session_token(self) -> None:
        self.session_token = secrets.token_hex(32)

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    profile_pic = db.Column(db.String(120), default='default.jpg')
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self) -> str:
        return f'<Message {self.username}: {self.content[:30]}...>'

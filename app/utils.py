from flask import current_app
from time import time

# In-memory rate limiting
last_message_time: dict[int, float] = {}
RATE_LIMIT_SECONDS = 0.8


def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def check_rate_limit(user_id: int) -> bool:
    """
    Check if user can send a message based on rate limit.
    Returns True if allowed, False if rate limited.
    """
    now = time()
    if user_id in last_message_time and now - last_message_time[user_id] < RATE_LIMIT_SECONDS:
        return False
    last_message_time[user_id] = now
    return True
